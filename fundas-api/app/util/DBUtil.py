import datetime

from app.blueprints.api.models import Technicals, \
    TechnicalsHistorical
from app.extensions import db
import pandas as pd
import time

from sqlalchemy import create_engine



def to_json(model):
    """ Returns a JSON representation of an SQLAlchemy-backed object.
    """
    json = {}
    for col in model._sa_class_manager.mapper.mapped_table.columns:
        json[col.name] = getattr(model, col.name)

    del json['created_on']
    del json['updated_on']

    return json


def bulk_insert_technical_data(ret_list):
    print(f"Persisting {len(ret_list)} entries")
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


    if tech_list:
        db.engine.execute(Technicals.__table__.insert(), tech_list)
    if hist_list:
        db.engine.execute(TechnicalsHistorical.__table__.insert(), hist_list)

    _log_status(len(tech_list), Technicals)
    _log_status(len(hist_list), TechnicalsHistorical)


def get_engine():
    engine = db.engine
    if not engine:
        try:
            from instance.settings import SQLALCHEMY_DATABASE_URI
            uri = SQLALCHEMY_DATABASE_URI
        except ImportError as ex:
            from config.settings import SQLALCHEMY_DATABASE_URI
            uri = SQLALCHEMY_DATABASE_URI

        engine = create_engine(uri)
        print(f"DB URI is {uri}")
    return engine


def get_technicals_as_df(symbol):
    tech = get_technicals(symbol)
    query = db.session.query(TechnicalsHistorical).join(Technicals).filter(Technicals.symbol==tech.symbol)
    return pd.read_sql(query.statement, db.session.bind, index_col='date', parse_dates=['date']).fillna(0)


def get_technicals(symbol):
    # print(f"Getting technicals for {symbol}")
    tech = Technicals.query.get(symbol)
    current_datetime = datetime.datetime.utcnow()
    if not tech:
        print(f"Technical data not available for {symbol}")
        tech = update_technicals(symbol)
    else:
        d1_ts = time.mktime(current_datetime.timetuple())
        d2_ts = time.mktime(tech.updated_on.timetuple())
        time_elapsed = (d1_ts - d2_ts)/60
        # print(f"{symbol} was updated {time_elapsed} minutes ago.")
        if time_elapsed > float(7 * 60 * 24):
            tech = update_technicals(symbol)
    return tech


def update_technicals(symbol):
    from app.util import DataAccess
    ret_dict = DataAccess.get_technicals(symbol)
    tech = Technicals.query.get(symbol)
    if tech:
        tech.query.delete()
        db.session.commit()
    bulk_insert_technical_data([ret_dict])
    return Technicals.query.get(symbol)


def _log_status(count, model_label):
    print('Created {} {}'.format(count, model_label))
