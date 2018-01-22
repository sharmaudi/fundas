import datetime
import numpy as np
import pandas as pd
import quandl
import redis
# Init Redis
from app.blueprints.api.models import CompanyInfo
from app.util import DBUtil

r = redis.StrictRedis(host='redis', port=6379, db=1)

r_full = redis.StrictRedis(host='redis', port=6379, db=3)

BROKER_URL = 'redis://redis:6379/2'

q_api_key = 'R27JMJXy2W-fLV6LX48P'

screener_name_mismatch = {
    'AVANTI': 'AVANTIFEED',
    'POKARNA': '532486',
    'GKB': '533212',
    'ORICON': 'ORICONENT',
    'TPLPLAST': 'TPLPLASTEH',
    'IBSEC': 'IBVENTURES',
    'SHIRPURG': 'SHIRPUR-G',
    'HCLINSYS': 'HCL-INSYS',
    'ILFSTRANS': 'IL&FSTRANS',
    'LTFH': 'L&TFH'
}

quandl_name_mismatch = {
    'AVANTI': 'AVANTIFEED',
    'ORICON': 'ORICONENT',
    'TPLPLAST': 'TPLPLASTEH',
    'IBSEC': 'IBVENTURES',
    'SHIRPURG': 'SHIRPUR-G',
    'HCLINSYS': 'HCL-INSYS'

}

indicators_available_quarterly = [
    'ETR',
    'DEP',
    'EBIDT',
    'EPS',
    'EBIDTSH',
    'TAX',
    'INT',
    'NP',
    'SHARE',
    'OP',
    'OI',
    'SR',
    'REVSH',
    'DIV',
    'EBIDTPCT',
    'IBTPCT',
    'NETPCT',
    'OPMSH',
    'OPMPCT',
    'LBETA',
    'MCAP',
    'BSEVOL',
    'BSEC',
    'BSEH',
    'BSEL',
    'BSEO',
    'NNPARAT',
    'GNPARAT',
    'FV',
    'ATM',
    'NIM',
    'MIPL',
    'CAPADQ',
    'OEXPNS',
    'PATBC',
    'CASARAT',
    'PBDT',
    'TIER1',
    'TIER2',
    'EPSEXC',
    'EXCEP',
    'PROVCOV',
    'CASA',
    'GNPA',
    'BRANCH',
    'PROV',
    'NNPA',
    'TI',
    'ASSOC'
]


def get_company_code(code, is_bse=False):
    sql = "SELECT symbol, {} FROM company_info where {} = %s"
    engine = DBUtil.get_engine()

    if is_bse:
        sql = sql.format('bse_code', 'bse_code')
    else:
        sql =sql.format('nse_code', 'nse_code')

    df = pd.read_sql(sql,engine,params=[code])
    return df.to_dict(orient='records')



def get_company_dataframe(company_name, info=None, latest_standalone=None, latest_consolidated=None):
    sql = "SELECT * FROM {} WHERE symbol=%s"

    engine = DBUtil.get_engine()

    df_a_s = pd.read_sql(sql.format('annual_standalone'),
                         engine,
                         params=[company_name],
                         parse_dates=['date']
                         ).set_index('date')

    df_a_c = pd.read_sql(sql.format('annual_consolidated'),
                         engine,
                         params=[company_name],
                         parse_dates=['date']
                         ).set_index('date')

    df_q_s = pd.read_sql(sql.format('quarterly_standalone'),
                         engine,
                         params=[company_name],
                         parse_dates=['date']
                         ).set_index('date')

    df_q_c = pd.read_sql(sql.format('quarterly_consolidated'),
                         engine,
                         params=[company_name],
                         parse_dates=['date']
                         ).set_index('date')

    return {
        'annual_standalone': df_a_s,
        'annual_consolidated': df_a_c,
        'quarterly_standalone': df_q_s,
        'quarterly_consolidated': df_q_c
    }


def get_data(company_name, company_dfs=None, indicators=None):

    if not company_dfs:
        company_dfs = get_company_dataframe(company_name, indicators)

    df_a_s = company_dfs['annual_standalone'].reset_index().set_index('date_str').drop('date', 1)

    df_a_c = company_dfs['annual_consolidated'].reset_index().set_index('date_str').drop('date', 1)

    df_q_s = company_dfs['quarterly_standalone'].reset_index().set_index('date_str').drop('date', 1)

    df_q_c = company_dfs['quarterly_consolidated'].reset_index().set_index('date_str').drop('date', 1)

    if not indicators:
        return {
            'annual_standalone': {
                'index': df_a_s.transpose().index.tolist(),
                'data': df_a_s.transpose().to_dict(orient='split')
            },
            'annual_consolidated': {
                'index': df_a_c.transpose().index.tolist(),
                'data': df_a_c.transpose().to_dict(orient='split')
            },
            'quarterly_standalone': {
                'index': df_q_s.transpose().index.tolist(),
                'data': df_q_s.transpose().to_dict(orient='split')
            },
            'quarterly_consolidated': {
                'index': df_q_c.transpose().index.tolist(),
                'data': df_q_c.transpose().to_dict(orient='split')
            }
        }
    else:
        df_a_s = df_a_s[indicators]
        df_a_c = df_a_c[indicators]
        result = {
            'annual_standalone': {
                'index': df_a_s.transpose().index.tolist(),
                'data': df_a_s.transpose().to_dict(orient='split')
            },
            'annual_consolidated': {
                'index': df_a_c.transpose().index.tolist(),
                'data': df_a_c.transpose().to_dict(orient='split')
            }
        }

        q_indicators = [i for i in indicators if i in indicators_available_quarterly]

        if q_indicators:
            df_q_s = df_q_s[q_indicators]
            df_q_c = df_q_c[q_indicators]
            result.update({
                'quarterly_standalone': {
                    'index': df_q_s.transpose().index.tolist(),
                    'data': df_q_s.transpose().to_dict(orient='split')
                },
                'quarterly_consolidated': {
                    'index': df_q_c.transpose().index.tolist(),
                    'data': df_q_c.transpose().to_dict(orient='split')
                }
            })
        return result


def get_featured_companies(location='/dropbox'):
    company_list = []
    ticker_list = []
    featured = [f'{location}/watchlist_bse.tls',
                               f'{location}/watchlist.tls']
    for list in featured:
        ticker_list += [line.rstrip('\n') for line in open(list)]
    for ticker in ticker_list:
        is_bse = False
        if ticker.isnumeric():
            is_bse = True
        l = get_company_code(ticker, is_bse)
        if l:
            comp = l[0]['symbol']
            if comp not in company_list:
                company_list.append(comp)
        else:
            print(f"Ticker {ticker} not found in database")
    return company_list


def get_all_symbols():
    sql = "SELECT symbol FROM latest_s_a"
    engine = DBUtil.get_engine()
    return pd.read_sql(sql, engine)['symbol'].tolist()


def get_momentum(company, start_date):
    info = CompanyInfo.query.get(company)
    is_bse=False
    print(f"Searching for company {company}")
    print(f"Company is {info}")

    if not info:
        key = f"NSE/{company}"
    elif info.nse_code:
        key = f'NSE/{info.nse_code}'
    else:
        is_bse = True
        key = f'BSE/BOM{info.bse_code}'
    print("Key is : {}".format(key))

    try:
        df = quandl.get(key,
                        authtoken=q_api_key,
                        returns='pandas',
                        start_date=start_date,
                        end_date=datetime.datetime.now().strftime('%Y-%m-%d'))
    except Exception as err:
        print(f"Key {key} not found in Quandl.")
        if key.split('/')[0] == 'NSE':
            print("Trying BSE")
            bse_key = f'BSE/BOM{info.bse_code}'
            is_bse = True
            df = quandl.get(bse_key,
                            authtoken=q_api_key,
                            returns='pandas',
                            start_date=start_date,
                            end_date=datetime.datetime.now().strftime('%Y-%m-%d'))

    if is_bse:
        df = df.rename(columns={'No. of Shares':'Volume'})
    else:
        df = df.rename(columns={'Total Trade Quantity': 'Volume'})
    return df.dropna()


def get_technicals(company, start_date="2012-12-31"):
    ret_dict = {}

    mom_df = get_momentum(company, start_date=start_date)

    mom_df['hhv_52'] = mom_df.High.rolling(window=52, min_periods=1, center=False).max()
    mom_df['hhv_all_time'] = mom_df.High.rolling(window=len(mom_df), min_periods=1, center=False).max()
    mom_df['roc_30'] = mom_df.Close.pct_change(periods=30) * 100
    mom_df['roc_60'] = mom_df.Close.pct_change(periods=60) * 100

    mom_df = mom_df.fillna(0)

    ret_dict.update({'technicals': mom_df})
    ret_dict.update({'company': company})

    return ret_dict



