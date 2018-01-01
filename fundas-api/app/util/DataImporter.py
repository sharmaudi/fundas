import concurrent.futures

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.types import Date
from app.util import DBUtil

import time

from app.util import DBUtil

engine = DBUtil.get_engine()


def read_tickers_csv(file_name='../../data/deb_tickers.csv', names=None, header=None):
    return pd.read_csv(file_name, names=names, header=header)


def read_deb_csv(file_name='../data/DEB_test.csv',
                 header=None,
                 names=None,
                 chunksize=None
                 ):

    if not names:
        names = ['lookup', 'date',
                        'standalone', 'consolidated']

    if chunksize:
        return pd.read_csv(file_name,
                           header=header,
                           names=names,
                           chunksize=chunksize)
    else:
        return pd.read_csv(file_name,
                           header=header,
                           names=names)


def init_db_with_chunks(file_name,
                           engine=None,
                           db_host='localhost',
                           db_port=5432,
                           db_pass='devpassword',
                           num_processors=2,
                            chunk_size=None):
    print("Not Implemented yet..")


def init_db_without_chunks(file_name,
                           engine=None,
                           db_host='localhost',
                           db_port=5432,
                           db_pass='devpassword',
                           num_processors=2):
    print(f"Reading CSV file {file_name}..")
    df = read_deb_csv(file_name)

    if not engine:
        engine = DBUtil.get_engine()

    print(f"Massaging fields..")
    df['symbol'] = df['lookup'].apply(lambda x: x.split('_', 2)[0])
    df['period'] = df['lookup'].apply(lambda x: x.split('_', 2)[1])
    df['indicator'] = df['lookup'].apply(lambda x: x.split('_', 2)[2])

    print(f"Creating dataframes..")
    all_annual = df[df.period == 'A']
    all_quarterly = df[df.period == 'Q']

    all_std_annual = all_annual[['symbol', 'indicator', 'date', 'standalone', 'period']]
    all_con_annual = all_annual[['symbol', 'indicator', 'date', 'consolidated', 'period']]
    all_std_q = all_quarterly[['symbol', 'indicator', 'date', 'standalone', 'period']]
    all_con_q = all_quarterly[['symbol', 'indicator', 'date', 'consolidated', 'period']]

    n1 = "AnnualStandalone"
    n2 = "AnnualConsolidated"
    n3 = "QuarterlyStandalone"
    n4 = "QuarterlyConsolidated"

    all_std_annual.name = n1
    all_con_annual.name = n2
    all_std_q.name = n3
    all_con_q.name = n4

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_processors) as executor:
        std_annual_fut = executor.submit(process_db_frame,
                                         all_std_annual,
                                         n1,
                                         'annual_standalone',
                                         True
                                         )
        con_annual_fut = executor.submit(process_db_frame,
                                         all_con_annual,
                                         n2,
                                         'annual_consolidated',
                                         False
                                         )
        std_q_fut = executor.submit(process_db_frame,
                                    all_std_q,
                                    n3,
                                    'quarterly_standalone',
                                    True
                                    )
        con_q_fut = executor.submit(process_db_frame,
                                    all_con_q,
                                    n4,
                                    'quarterly_consolidated',
                                    False
                                    )
        df_future_map = {
            std_annual_fut: n1,
            con_annual_fut: n2,
            std_q_fut: n3,
            con_q_fut: n4
        }

        for future in concurrent.futures.as_completed(df_future_map):
            future_df_name = df_future_map[future]
            try:
                result = future.result()
                print(result)
            except Exception as exc:
                print(f"Exception while processing future for {future_df_name}")
                print(exc)


def process_db_frame(df, df_name, table_name, standalone=False):
    if standalone:
        value = 'standalone'
    else:
        value = 'consolidated'

    print(f"[{df_name}]Processing for {value} data..")
    a_s_p = pd.pivot_table(df,
                           index=['date', 'symbol', 'period'],
                           columns=['indicator'],
                           values=value).reset_index().sort_values(['symbol',
                                                                    'date'])

    a_s_p['date_str'] = a_s_p['date'].apply(lambda x: int(time.mktime(time.strptime(x, "%Y-%m-%d")) * 1000))

    print(f"[{df_name}]Provisioning to database table: {table_name}..")
    a_s_p.to_sql(table_name,
                 engine,
                 if_exists='replace',
                 index_label='id',
                 dtype={'date': Date})
    print(f"[{df_name}]Done!")
    return {
        'name': df_name,
        'status': 'success'
    }


def init_db(file_name='../data/DEB_test.csv', chunks=None):
    if not chunks:
        init_db_without_chunks(file_name)
    else:
        init_db_with_chunks(file_name, chunk_size=chunks)



if __name__ == "__main__":
    init_db('../../data/DEB.csv')
