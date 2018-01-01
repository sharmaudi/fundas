import concurrent.futures
import datetime

import click

from app.app import create_app
from app.blueprints.api.models import CompanyInfo, LatestStandalone, LatestConsolidated, Technicals, \
    TechnicalsHistorical
from app.extensions import db
from app.util import ScreenerUtil, DataImporter, DataAccess, DBUtil
from app.util.PathResolver import resolve_data
import json
# Create an app context for the database connection.

app = create_app()
db.app = app

views_sql = """
create MATERIALIZED VIEW latest_c_a as
  SELECT  DISTINCT  on ("symbol") *
  from annual_consolidated
  ORDER BY "symbol", "date" DESC NULLS LAST;

create MATERIALIZED VIEW latest_s_a as
  SELECT  DISTINCT  on ("symbol") *
  from annual_standalone
  ORDER BY "symbol", "date" DESC NULLS LAST;

create MATERIALIZED VIEW latest_c_q as
  SELECT  DISTINCT  on ("symbol") *
  from quarterly_consolidated
  ORDER BY "symbol", "date" DESC NULLS LAST;

create MATERIALIZED VIEW latest_s_q as
  SELECT  DISTINCT  on ("symbol") *
  from quarterly_standalone
  ORDER BY "symbol", "date" DESC NULLS LAST

CREATE UNIQUE INDEX idx_symbol_c_a on latest_c_a(symbol);
CREATE UNIQUE INDEX idx_symbol_s_a on latest_s_a(symbol);
CREATE UNIQUE INDEX idx_symbol_c_q on latest_c_q(symbol);
CREATE UNIQUE INDEX idx_symbol_s_q on latest_c_q(symbol);
"""


@click.group()
def cli():
    """ Run PostgreSQL related tasks. """
    pass


@click.command()
def init():
    """
    Initialize the database.
    :param with_testdb: Create a test database
    :return: None
    """
    db.drop_all()
    db.create_all()

    print(CompanyInfo.__table__.columns.keys())

    _import_company_info()
    return None


def _import_company_info():
    names = ['isin_code',
             'bse_code',
             'bse_id',
             'bse_name',
             'nse_code',
             'nse_name',
             'sector',
             'industry',
             'quandl_code']

    csv_df = DataImporter.read_tickers_csv(resolve_data('deb_tickers.csv'), names=names, header=0)

    created_on = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    csv_df['symbol'] = csv_df.quandl_code
    csv_df['created_on'] = created_on
    csv_df['updated_on'] = created_on
    csv_df = csv_df.replace(to_replace=['NM'], value=[None])
    csv_df['screener_code'] = csv_df[['nse_code', 'bse_code']].apply(get_screener_code, axis=1)
    records = csv_df.to_dict(orient='records')
    _bulk_insert(CompanyInfo, records, "company records")


def get_screener_code(row):
    if row['nse_code']:
        return row['nse_code']
    else:
        return row['bse_code']


def _bulk_insert(model, data, label):
    with app.app_context():
        model.query.delete()

        db.session.commit()
        db.engine.execute(model.__table__.insert(), data)

        _log_status(model.query.count(), label)

    return None


@click.command()
def get_companies():
    all_companies = CompanyInfo.query.with_entities(CompanyInfo.symbol, CompanyInfo.screener_code).all()
    print(all_companies)
    return all_companies


def _bulk_upload(model_list,
                 function_to_execute,
                 function_to_upload,
                 delete_existing=False,
                 batch_size=100,
                 max_workers=8,
                 company_list=None
                 ):
    print(f"Processing bulk upload")

    if delete_existing:
        for model in model_list:
            print(f"[{model} Deleting Model.]")
            model.query.delete()
        db.session.commit()

    all_symbols = CompanyInfo.query.all()

    result_list = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_score = {}
        error_list = []

        for tup in all_symbols:
            if tup.symbol in company_list:
                future_score.update(
                    {executor.submit(function_to_execute,
                                     DBUtil.to_json(tup)): tup.symbol})

        for future in concurrent.futures.as_completed(future_score):
            c = future_score[future]
            try:
                result_list.append(future.result(timeout=600))

                if len(result_list) > batch_size:
                    function_to_upload(result_list)
            except Exception as e:
                print(f"[{model_list}]Exception while processing [{c}]. Exception: {e}")
                error_list.append(future_score[future])

        function_to_upload(result_list)


@click.command()
def load_the_lot():
    print("Loading from screener. Will take time")

    LatestStandalone.query.delete()
    LatestConsolidated.query.delete()
    db.session.commit()

    all_symbols = CompanyInfo.query.with_entities(CompanyInfo.symbol).all()

    symbol_list = [tup.symbol for tup in all_symbols]
    print(symbol_list)
    _bulk_upload([LatestConsolidated, LatestStandalone],
                 get_screener_dicts,
                 bulk_insert_screener,
                 company_list=symbol_list[:10]
                )

    # _bulk_upload([],
    #              get_momentum,
    #              bulk_insert_technical_data,
    #              company_list=symbol_list[:10]
    #              )


def bulk_insert_screener(result_list):
    st_list = []
    c_list = []
    for result in result_list:
        st_list.append(result['standalone'])
        c_list.append(result['consolidated'])
    with app.app_context():
        if st_list:
            db.engine.execute(LatestStandalone.__table__.insert(), st_list)
        if c_list:
            db.engine.execute(LatestConsolidated.__table__.insert(), c_list)

    _log_status(LatestStandalone.query.count(), LatestStandalone)
    _log_status(LatestConsolidated.query.count(), LatestConsolidated)
    return None


def _log_status(count, model_label):
    click.echo('Created {0} {1}'.format(count, model_label))
    return None


def get_momentum(info_dict):
    symbol = info_dict['symbol']
    ret_dict = DataAccess.get_technicals(symbol)
    return ret_dict


def bulk_insert_technical_data(ret_list):
    print(f"Persisting ${ret_list}")

    created_on = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')

    tech_list = []
    hist_list = []
    for rec in ret_list:
        df = rec['technicals']
        tech_list.append(
            {
                'created_on': created_on,
                'updated_on': created_on,
                'symbol': rec['company'],
                'latest_price': df.iloc[-1].Close,
                'splits': {},
                'roc30': df.iloc[-1].roc_30,
                'roc60': df.iloc[-1].roc_60,
                'hhv52': df.iloc[-1].hhv_52,
                'hhv_all_time': df.iloc[-1].hhv_all_time,
            }

        )

        for index, row in df.iterrows():
            hist_list.append(
                {
                    'created_on': created_on,
                    'updated_on': created_on,
                    'symbol': rec['company'],
                    'date': index.strftime('%Y-%m-%d'),
                    'open': row['Open'],
                    'high': row['High'],
                    'close': row['Close'],
                    'low': row['Low'],
                    'volume': row['Volume'],
                    'roc30': row['roc_30'],
                    'roc60': row['roc_60'],
                    'hhv52': row['hhv_52'],
                    'hhv_all_time': row['hhv_all_time']

                }
            )

    with app.app_context():
        if tech_list:
            db.engine.execute(Technicals.__table__.insert(), tech_list)
        if hist_list:
            db.engine.execute(TechnicalsHistorical.__table__.insert(), hist_list)

    _log_status(Technicals.query.count(), Technicals)
    _log_status(TechnicalsHistorical.query.count(), TechnicalsHistorical)


def get_screener_dicts(info_dict):
    l_s = {}
    l_c = {}
    created_on = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')

    symbol = info_dict['symbol']
    screener_code = info_dict['screener_code']
    bse_code = info_dict['bse_code']

    l_s['symbol'] = symbol
    l_s['book_value'] = None
    l_s['current_price'] = None
    l_s['face_value'] = None
    l_s['market_cap'] = None
    l_s['price_to_earning'] = None
    l_s['created_on'] = created_on
    l_s['updated_on'] = created_on
    l_s['analysis'] = None

    l_c['symbol'] = symbol
    l_c['book_value'] = None
    l_c['current_price'] = None
    l_c['face_value'] = None
    l_c['market_cap'] = None
    l_c['price_to_earning'] = None
    l_c['created_on'] = created_on
    l_c['updated_on'] = created_on
    l_c['analysis'] = None

    try:
        print(f"{symbol}|{screener_code}|{bse_code} - Processing")
        d = ScreenerUtil.get_screener_dicts(screener_code=screener_code, bse_code=bse_code)

        l_s['symbol'] = symbol
        l_s['book_value'] = d['standalone']['book_value']
        l_s['current_price'] = d['standalone']['current_price']
        l_s['face_value'] = d['standalone']['face_value']
        l_s['market_cap'] = d['standalone']['market_capitalization']
        l_s['price_to_earning'] = d['standalone']['price_to_earning']
        l_s['analysis'] = d['standalone']['analysis']
        l_s['created_on'] = created_on
        l_s['updated_on'] = created_on

        l_c['symbol'] = symbol
        l_c['book_value'] = d['consolidated']['book_value']
        l_c['current_price'] = d['consolidated']['current_price']
        l_c['face_value'] = d['consolidated']['face_value']
        l_c['market_cap'] = d['consolidated']['market_capitalization']
        l_c['price_to_earning'] = d['consolidated']['price_to_earning']
        l_c['analysis'] = d['consolidated']['analysis']
        l_c['created_on'] = created_on
        l_c['updated_on'] = created_on
    except Exception as e:
        f"Exception while getting details from screener for {symbol}. Exeption: {e}"

    return {
        'standalone': l_s,
        'consolidated': l_c
    }


def get_technicals():
    d = DataAccess.get_technicals('AFEL')
    print(d)


@click.command()
def test():
    d = ScreenerUtil.get_screener_dicts(CompanyInfo.query.get('ITC'))
    print(d)


@click.command()
def import_deb():
    DataImporter.init_db(resolve_data('DEB.csv'))


cli.add_command(init)
cli.add_command(get_companies)
cli.add_command(load_the_lot)
cli.add_command(test)
cli.add_command(import_deb)

if __name__ == '__main__':
    cli()
