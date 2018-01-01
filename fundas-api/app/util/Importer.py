import concurrent.futures
import csv
import sqlite3
import time

import pandas as pd
import redis
from sqlalchemy import Table, Column, Integer, String, MetaData, Float, select, distinct
from sqlalchemy import create_engine

r_full = redis.StrictRedis(host='redis', port=6379, db=3)
engine = create_engine('postgresql://fundas:devpassword@postgres:5432/fundas')
metadata = MetaData()
fundas = Table('fundas', metadata,
               Column('id', Integer, primary_key=True),
               Column('symbol', String),
               Column('period', String),
               Column('indicator', String),
               Column('date', String),
               Column('standalone', Float),
               Column('consolidated', Float),
               )


def create_db():
    global engine
    global metadata
    global fundas
    try:
        metadata.drop_all(engine)
    except Exception as e:
        print(f"Exception: {e}")
    metadata.create_all(engine)
    return fundas


def chunkify():
    chunks = []
    for i, chunk in enumerate(pd.read_csv('data/DEB.csv', header=0,index_col=False, chunksize=500000)):
        chunk_name = f"data/CHUNK-DEB-{i}.csv"
        chunk.to_csv(chunk_name, header=None, index=None)
        chunks.append(chunk_name)
    print(f"Chunks created {chunks}")
    return chunks


def process_file(filename, batch_size=250000):
    print(f"Processing file {filename}")
    count = 0
    conn = engine.connect()
    batch = []
    with open(filename) as csvfile:
        spm = csv.reader(csvfile)
        for row in spm:
            comp = row[0].split('_')[0]
            period = row[0].split('_')[1]
            indicator = row[0].split('_')[2]
            new_ind = indicator
            if len(row[0].split('_')) > 3:
                for a in row[0].split('_')[3:]:
                    new_ind = new_ind + '_' + a
            indicator = new_ind
            date = row[1]
            value1 = row[2] if row[2] else None
            value2 = row[3] if row[3] else None

            batch.append(
                {
                    'symbol': comp,
                    'period': period,
                    'indicator': indicator,
                    'date': date,
                    'standalone': value1,
                    'consolidated': value2
                }
            )

            if len(batch) >= batch_size:
                conn.execute(fundas.insert(), batch)
                batch = []
                count += 1
                print(f"File: {filename}, Records Processed : {count * batch_size}")
    conn.close()


def import_deb_postgres():
    chunks = chunkify()

    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        future_to_file = {executor.submit(process_file, file): file for file in chunks}
        for future in concurrent.futures.as_completed(future_to_file):
            file = future_to_file[future]
            try:
                data = future.result()
            except Exception as exc:
                print(f"Exception while processing file {file}: {exc}")
            else:
                print(f"File Processed: {file}")


def import_deb():
    con = sqlite3.connect('test.db')
    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS FUNDAS")

    cur.execute(
        "CREATE TABLE FUNDAS (symbol TEXT, period TEXT, indicator TEXT, date TEXT,"
        " standalone REAL, consolidated REAL);")

    count = 0

    with open('data/DEB.csv') as csvfile:
        spm = csv.reader(csvfile)
        for row in spm:
            comp = row[0].split('_')[0]
            period = row[0].split('_')[1]
            indicator = row[0].split('_')[2]
            new_ind = indicator
            if len(row[0].split('_')) > 3:
                for a in row[0].split('_')[3:]:
                    new_ind = new_ind + '_' + a
            indicator = new_ind
            date = row[1]
            value1 = row[2]
            value2 = row[3]
            cur.execute("INSERT INTO FUNDAS VALUES (?,?,?,?,?,?)", (comp, period, indicator, date, value1, value2))
            count += 1
            if count % 100000 == 0:
                progress = count / 7301389 * 100
                print('{} percent complete. {} records imported'.format(progress, count))

    con.commit()
    con.close()


# Clear the Redis caches
def flush_redis_cache():
    r = redis.StrictRedis(host='redis', port=6379, db=1)
    r.flushall()


def create_redis_database(create_quarterly=False):
    if create_quarterly:
        identifier = 'A'
    else:
        identifier = 'Q'
    conn = sqlite3.connect('test.db')
    query = 'SELECT * FROM FUNDAS WHERE period=?'
    params = [identifier]
    num = 0
    for big_frame in pd.read_sql(query, con=conn, params=params, parse_dates=['date'], chunksize=5000):
        num += 1
        grouped = big_frame.groupby('symbol')
        i = 0
        total_symbols = len(grouped)
        for g, df in grouped:
            i += 1
            pivot_standalone = df.pivot(index='date', columns='indicator', values='standalone')
            pivot_consolidated = df.pivot(index='date', columns='indicator', values='consolidated')
            r_full.set(g + "_" + identifier + "_STANDALONE", pivot_standalone.to_json())
            r_full.set(g + "_" + identifier + "_CONSOLIDATED", pivot_consolidated.to_json())
            progress = (i / total_symbols) * 100
            print('Chunk: {0}, Progress: {1:.2f}'.format(num, progress))


def get_all_companies():
    con = engine.connect()
    s = select([distinct(fundas.c.symbol)])
    return_set = con.execute(s)
    companies = [row[0] for row in return_set]
    return companies


def init_redis():
    start = time.clock()
    print("Getting all companies from DB")
    all_companies = get_all_companies()
    print("Done. Time Taken: {}".format(time.clock() - start))

    total = len(all_companies)
    print(f"Total companies: {total}")


    #process these many companies at once
    chunk_size = 50

    all_companies_chunks = [all_companies[i:i + chunk_size] for i in range(0, len(all_companies), chunk_size)]


    start = time.clock()
    success = 0
    error = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        for result in executor.map(create_company_in_redis, all_companies_chunks):
            if result['imported']:
                success += len(result['company_list'])
            else:
                error += 1
            print(f"{success}/{total} imported. {error} errors")

    print("All Done. Total Time Taken: {}".format(time.clock() - start))


def create_company_in_redis(company_list, create_quarterly=False):
    con = engine.raw_connection()
    print(f"Processing {company_list}")
    start = time.clock()
    query = 'SELECT * FROM FUNDAS WHERE period=%s AND symbol IN %s'

    if create_quarterly:
        identifier = 'Q'
    else:
        identifier = 'A'
    params = [identifier, tuple(company_list)]

    df_iter = pd.read_sql(query, con=con, params=params, parse_dates=['date'])
    num = 0
    for big_frame in df_iter:
        print(big_frame)
        num += 1
        grouped = big_frame.groupby('symbol')
        i = 0
        total_symbols = len(grouped)
        for g, df in grouped:
            i += 1
            pivot_standalone = df.pivot(index='date', columns='indicator', values='standalone')
            pivot_consolidated = df.pivot(index='date', columns='indicator', values='consolidated')
            r_full.set(g + "_" + identifier + "_STANDALONE", pivot_standalone.to_json())
            r_full.set(g + "_" + identifier + "_CONSOLIDATEtuple([company_list[0] for for in rows]))D", pivot_consolidated.to_json())

    # print(f"{company} imported. Time Taken: {time.clock() - start}")
    return {
        "company_list": company_list,
        "imported": True
    }


