from app.util import DataAccess
import pandas as pd



def perform_valuation_checks(df):
    df = df.sort_index(ascending=False)
    latest = get_latest_non_zero(df, ['PE', 'PEG', 'PBV', 'EVEBIDTA'])
    valuation_checks = [{
        'id': 'valuation_check1',
        'rule': 'PE Ratio < 20',
        'outcome': perform_operation('((latest.PE < 20).tolist()[0])', latest, df),
        'lhs': latest.PE.tolist()[0],
        'rhs': 20,
        'lcol': 'PE Ratio',
        'rcol': None
    }, {
        'id': 'valuation_check2',
        'rule': 'PE Ratio < 5 year average PE',
        'outcome': perform_operation('(latest.PE < df.head(5).PE.mean()).tolist()[0]', latest, df),
        'lhs': latest.PE.tolist()[0],
        'rhs': df.head(5).PE.mean(),
        'lcol': 'PE',
        'rcol': '5 Years avg PE'
    }, {
        'id': 'valuation_check3',
        'rule': 'PE Ratio < All time Average PE',
        'outcome': perform_operation('(latest.PE < df.PE.mean()).tolist()[0]', latest, df),
        'lhs': latest.PE.tolist()[0],
        'rhs': df.PE.mean(),
        'lcol': 'PE',
        'rcol': 'All time average PE'
    }, {
        'id': 'valuation_check4',
        'rule': 'PEG Ratio is within 0 and 1',
        'outcome': perform_operation('(latest.PEG < 1).tolist()[0] and (latest.PEG > 0).tolist()[0]', latest, df),
        'lhs': latest.PEG.tolist()[0],
        'rhs': [0, 1],
        'lcol': 'PEG Ratio',
        'rcol': None
    }, {
        'id': 'valuation_check5',
        'rule': 'Price to book value is less than 2',
        'outcome': perform_operation('(latest.PBV < 2).tolist()[0]', latest, df),
        'lhs': latest.PBV.tolist()[0],
        'rhs': 2,
        'lcol': 'Price to book ratio',
        'rcol': None
    }, {
        'id': 'valuation_check6',
        'rule': 'EV/EBITDA < 10',
        'outcome': perform_operation('(latest.EVEBIDTA < 10).tolist()[0]', latest, df),
        'lhs': latest.EVEBIDTA.tolist()[0],
        'rhs': 10,
        'lcol': 'EV/EBITDA',
        'rcol': None
    }
    ]

    return valuation_checks


def perform_performance_checks(df):
    df = df.sort_index(ascending=False)
    latest = get_latest_non_zero(df, [
        'CEPS',
        'EPS',
        'ROE',
        'ROCE',
        'ROA',
        'CROCI',
        'NETPCT'
    ])
    checks = [{
        'id': 'performance_check1',
        'rule': 'Cash EPS > EPS',
        'outcome': perform_operation('(latest.CEPS > latest.EPS).tolist()[0]', latest, df),
        'lhs': latest.CEPS.tolist()[0],
        'rhs': latest.EPS.tolist()[0],
        'lcol': 'Cash EPS',
        'rcol': 'EPS'
    }, {
        'id': 'performance_check2',
        'rule': 'EPS is greater than EPS 5 years ago',
        'outcome': perform_operation('latest.EPS.tolist()[0] > df.EPS.iloc[[5]].tolist()[0]', latest, df),
        'lhs': latest.EPS.tolist()[0],
        'rhs': df.EPS.iloc[[5]].tolist()[0],
        'lcol': 'EPS',
        'rcol': 'EPS 5 years ago'
    }, {
        'id': 'performance_check3',
        'rule': 'ROE is greater than 20%',
        'outcome': perform_operation('(latest.ROE * 100 > 20).tolist()[0]', latest, df),
        'lhs': (latest.ROE * 100).tolist()[0],
        'rhs': 20,
        'lcol': 'ROE',
        'rcol': None
    }, {
        'id': 'performance_check4',
        'rule': 'ROCE is greater than ROCE 3 years ago',
        'outcome': perform_operation('(latest.ROCE * 100).tolist()[0] > (df.ROCE * 100).iloc[[3]].tolist()[0]', latest, df),
        'lhs': (latest.ROCE * 100).tolist()[0],
        'rhs': (df.ROCE * 100).iloc[[3]].tolist()[0],
        'lcol': 'ROCE',
        'rcol': 'ROCE 3 years ago'
    }, {
        'id': 'performance_check5',
        'rule': 'ROA is greater than 10%',
        'outcome': perform_operation('(latest.ROA * 100 > 10).tolist()[0]', latest, df),
        'lhs': (latest.ROA * 100).tolist()[0],
        'rhs': 10,
        'lcol': 'ROA',
        'rcol': None
    }, {
        'id': 'performance_check6',
        'rule': 'ROA > 5 year average ROA',
        'outcome': perform_operation('(latest.ROA > df.head(5).ROA.mean()).tolist()[0]', latest, df),
        'lhs': perform_operation('latest.ROA.tolist()[0] * 100', latest, df),
        'rhs': df.head(5).ROA.mean() * 100,
        'lcol': 'ROA',
        'rcol': 'ROA 5 year avg.'
    }, {
        'id': 'performance_check7',
        'rule': 'CROCI > 3 year average CROCI',
        'outcome': perform_operation('(latest.CROCI > df.head(3).CROCI.mean()).tolist()[0]', latest, df),
        'lhs': perform_operation('latest.CROCI.tolist()[0] * 100', latest, df),
        'rhs': df.head(3).CROCI.mean() * 100,
        'lcol': 'CROCI',
        'rcol': 'CROCI 3 year avg.'
    }, {
        'id': 'performance_check8',
        'rule': 'Net Profit Margin > 3 year average Net Profit Margin',
        'outcome': perform_operation('(latest.NETPCT > df.head(3).NETPCT.mean()).tolist()[0]', latest, df),
        'lhs': perform_operation('latest.NETPCT.tolist()[0] * 100', latest, df),
        'rhs': df.head(3).NETPCT.mean() * 100,
        'lcol': 'Net Profit Margin',
        'rcol': 'NPM 3 years average'
    }
    ]
    return checks


def get_latest_non_zero(df, indicator_list=None):
    df = df.sort_index(ascending=False)
    latest = df.iloc[[0]]
    if indicator_list:
        test = df.iloc[[0]][indicator_list]
    else:
        test = df.iloc[[0]]

    if pd.isnull(test.all):
        latest = df.iloc[[1]]

    if (test == 0).all(axis=1).tolist()[0]:
        latest = df.iloc[[1]]

    return latest


def perform_operation(expression, latest, df):
        try:
            ret = eval(expression)
        except Exception as e:
            print(f"Exception while evaluating expression: ${expression}. Exception is ${e}")
            ret = False

        return ret


def perform_health_checks(df):
    df = df.sort_index(ascending=False)
    latest = get_latest_non_zero(df, [
        'CRATIO',
        'SOLRATIO',
        'LTDE',
        'IC',
        'DEBT_ASSETS',
        'CFO'
    ])
    checks = [{
        'id': 'health_check1',
        'rule': 'Current Ratio > 1',
        'outcome': perform_operation('(latest.CRATIO > 1).tolist()[0]', latest, df),
        'lhs': latest.CRATIO.tolist()[0],
        'rhs': 1,
        'lcol': 'Current Ratio',
        'rcol': None
    }, {
        'id': 'health_check2',
        'rule': 'Solvency Ratio > .2',
        'outcome': perform_operation('(latest.SOLRATIO > .2).tolist()[0]', latest, df),
        'lhs': latest.SOLRATIO.tolist()[0],
        'rhs': .2,
        'lcol': 'Solvency Ratio',
        'rcol': None
    }, {
        'id': 'health_check3',
        'rule': 'Solvency ratio is greater than Solvency ratio 3 years ago',
        'outcome': perform_operation('(latest.SOLRATIO).tolist()[0] > (df.SOLRATIO).iloc[[3]].tolist()[0]', latest, df),
        'lhs': (latest.SOLRATIO).tolist()[0],
        'rhs': (df.SOLRATIO).iloc[[3]].tolist()[0],
        'lcol': 'Solvency Ratio',
        'rcol': 'Solvency Ratio 3 years ago'
    }, {
        'id': 'health_check4',
        'rule': 'Debt to equity is less than Debt to equity 5 years ago',
        'outcome': perform_operation('(latest.LTDE).tolist()[0] < (df.LTDE).iloc[[5]].tolist()[0]', latest, df),
        'lhs': (latest.LTDE).tolist()[0],
        'rhs': (df.LTDE).iloc[[5]].tolist()[0],
        'lcol': 'Debt to Equity',
        'rcol': 'DE 5 years ago'
    }, {
        'id': 'health_check5',
        'rule': 'Debt to Equity < 1',
        'outcome': perform_operation('(latest.LTDE < 1).tolist()[0]', latest, df),
        'lhs': latest.LTDE.tolist()[0],
        'rhs': 1,
        'lcol': 'Debt to Equity',
        'rcol': None
    }, {
        'id': 'health_check6',
        'rule': 'Interest Coverage > 5',
        'outcome': perform_operation('(latest.IC > 5).tolist()[0]', latest, df),
        'lhs': latest.IC.tolist()[0],
        'rhs': 5,
        'lcol': 'Interest Coverage',
        'rcol': None
    }, {
        'id': 'health_check7',
        'rule': 'Debt to Assets < .7',
        'outcome': perform_operation('(latest.DEBT_ASSETS < .7).tolist()[0]', latest, df),
        'lhs': latest.DEBT_ASSETS.tolist()[0],
        'rhs': .7,
        'lcol': 'Debt to Assets',
        'rcol': None
    }, {
        'id': 'health_check8',
        'rule': 'Cash from operations 3 year average > Net profit 3 year average',
        'outcome': perform_operation('(df.CFO.head(3).mean() > df.NP.head(3).mean()).item()', latest, df),
        'lhs': df.CFO.head(3).mean(),
        'rhs': df.NP.head(3).mean(),
        'lcol': 'CFO 3 years avg.',
        'rcol': 'Net Profit 3 years avg.'
    }
    ]
    return checks


def perform_dividend_checks(df):
    df = df.sort_index(ascending=False)
    latest = get_latest_non_zero(df, ['DIV', 'DIVPAY', 'DIVYLD'])

    checks = [{
        'id': 'div_check1',
        'rule': 'Dividend yield > 3%',
        'outcome': perform_operation('(latest.DIVYLD > .03).tolist()[0]', latest, df),
        'lhs': perform_operation('latest.DIVYLD.tolist()[0] * 100', latest, df),
        'rhs': .03 * 100,
        'lcol': 'Dividend Yield',
        'rcol': None
    }, {
        'id': 'div_check2',
        'rule': 'Latest dividend increased more than 25% since 3 years ago',
        'outcome': perform_operation('(latest.DIV).tolist()[0] * .75 > (df.DIV).iloc[[3]].tolist()[0]', latest, df),
        'lhs': (latest.DIV).tolist()[0],
        'rhs': (df.DIV).iloc[[3]].tolist()[0],
        'lcol': 'Dividend',
        'rcol': 'Dividend 3 years ago'
    }, {
        'id': 'div_check3',
        'rule': 'Latest dividend increased more than 50% since 6 years ago',
        'outcome': perform_operation('(latest.DIV).tolist()[0] * .5 > (df.DIV).iloc[[6]].tolist()[0]', latest, df),
        'lhs': (latest.DIV).tolist()[0],
        'rhs': (df.DIV).iloc[[6]].tolist()[0],
        'lcol': 'Dividend',
        'rcol': 'Dividend 6 years ago'
    }, {
        'id': 'div_check4',
        'rule': 'Dividend payout between 10% and 60%',
        'outcome': perform_operation('(latest.DIVPAY > .1).tolist()[0] and (latest.DIVPAY < .6).tolist()[0]', latest, df),
        'lhs': latest.DIVPAY.tolist()[0] * 100,
        'lcol':'Dividend Payout',
        'rcol':None,
        'rhs': [10, 60]
    }

    ]

    return checks


def get_score_from_checks(checks):
    score = 0
    for check in checks:
        if check['outcome']:
            score += 1

    score_rounded = round(10 / len(checks) * score)
    return score_rounded


def analyse(company_name, company_dataframe=None):
    if not company_dataframe:
        company_dataframe = DataAccess.get_company_dataframe(company_name)

    return {
        'consolidated': analyse_company(company_name, company_dataframe, 'consolidated'),
        'standalone': analyse_company(company_name, company_dataframe, 'standalone')
    }


def analyse_company(company_name, company_dataframe=None, data_type='standalone'):
    if not company_dataframe:
        company_dataframe = DataAccess.get_company_dataframe(company_name)

    df = company_dataframe['annual_standalone']
    if data_type is 'consolidated':
        df = company_dataframe['annual_consolidated']

    result = {

    }

    valuation_checks = None
    score = None
    try:
        valuation_checks = perform_valuation_checks(df)
        score = get_score_from_checks(valuation_checks)
    except Exception as e:
        print(f"[{company_name}]Exception during valuation checks. Exception: {e}")
    result['valuation'] = {}
    result['valuation']['checks'] = valuation_checks
    result['valuation']['score'] = score

    p_checks = None
    score = None
    try:
        p_checks = perform_performance_checks(df)
        score = get_score_from_checks(p_checks)
    except Exception as e:
        print(f"[{company_name}]Exception during performance checks. Exception: {e}")
    result['performance'] = {}
    result['performance']['checks'] = p_checks
    result['performance']['score'] = score

    h_checks = None
    score = None
    try:
        h_checks = perform_health_checks(df)
        score = get_score_from_checks(h_checks)
    except Exception as e:
        print(f"[{company_name}]Exception during health checks. Exception: {e}")
    result['health'] = {}
    result['health']['checks'] = h_checks
    result['health']['score'] = score

    d_checks = None
    score = None
    try:
        d_checks = perform_dividend_checks(df)
        score = get_score_from_checks(d_checks)
    except Exception as e:
        print(f"[{company_name}]Exception during dividend checks. Exception: {e}")
    result['dividends'] = {}
    result['dividends']['checks'] = d_checks
    result['dividends']['score'] = score

    return result

