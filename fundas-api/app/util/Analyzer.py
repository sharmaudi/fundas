import concurrent.futures
import csv

from flask import current_app

from app.blueprints.api.models import CompanyInfo
from app.util import DataAccess, DBUtil
import pandas as pd

from app.util.PathResolver import resolve_data


def perform_valuation_checks(df, silent=False):
    df = df.sort_index(ascending=False)
    latest = get_latest_non_zero(df, ['PE', 'PEG', 'PBV', 'EVEBIDTA'])
    valuation_checks = [{
        'id': 'valuation_check1',
        'rule': 'PE Ratio < 20',
        'outcome': perform_operation('((latest.PE < 20).tolist()[0])', latest, df, silent=silent),
        'lhs': eval_expr('latest.PE.tolist()[0]', latest, df),
        'rhs': 20,
        'lcol': 'PE Ratio',
        'rcol': None
    }, {
        'id': 'valuation_check2',
        'rule': 'PE Ratio < 5 year average PE',
        'outcome': perform_operation('(latest.PE < df.head(5).PE.mean()).tolist()[0]', latest, df, silent=silent),
        'lhs': eval_expr('latest.PE.tolist()[0]', latest, df),
        'rhs': eval_expr('df.head(5).PE.mean()', latest, df),
        'lcol': 'PE',
        'rcol': '5 Years avg PE'
    }, {
        'id': 'valuation_check3',
        'rule': 'PE Ratio < All time Average PE',
        'outcome': perform_operation('(latest.PE < df.PE.mean()).tolist()[0]', latest, df, silent=silent),
        'lhs': eval_expr('latest.PE.tolist()[0]', latest, df),
        'rhs': eval_expr('df.PE.mean()', latest, df),
        'lcol': 'PE',
        'rcol': 'All time average PE'
    }, {
        'id': 'valuation_check4',
        'rule': 'PEG Ratio is within 0 and 1',
        'outcome': perform_operation('(latest.PEG < 1).tolist()[0] and (latest.PEG > 0).tolist()[0]', latest, df, silent=silent),
        'lhs': eval_expr('latest.PEG.tolist()[0]', latest, df),
        'rhs': [0, 1],
        'lcol': 'PEG Ratio',
        'rcol': None
    }, {
        'id': 'valuation_check5',
        'rule': 'Price to book value is less than 2',
        'outcome': perform_operation('(latest.PBV < 2).tolist()[0]', latest, df, silent=silent),
        'lhs': eval_expr('latest.PBV.tolist()[0]', latest, df),
        'rhs': 2,
        'lcol': 'Price to book ratio',
        'rcol': None
    }, {
        'id': 'valuation_check6',
        'rule': 'EV/EBITDA < 10',
        'outcome': perform_operation('(latest.EVEBIDTA < 10).tolist()[0]', latest, df, silent=silent),
        'lhs': eval_expr('latest.EVEBIDTA.tolist()[0]', latest, df),
        'rhs': 10,
        'lcol': 'EV/EBITDA',
        'rcol': None
    }
    ]

    return valuation_checks


def perform_performance_checks(df, silent=False):
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
        'outcome': perform_operation('(latest.CEPS > latest.EPS).tolist()[0]', latest, df, silent=silent),
        'lhs': eval_expr('latest.CEPS.tolist()[0]', latest, df),
        'rhs': eval_expr('latest.EPS.tolist()[0]', latest, df),
        'lcol': 'Cash EPS',
        'rcol': 'EPS'
    }, {
        'id': 'performance_check2',
        'rule': 'EPS is greater than EPS 5 years ago',
        'outcome': perform_operation('latest.EPS.tolist()[0] > df.EPS.iloc[[5]].tolist()[0]', latest, df, silent=silent),
        'lhs': eval_expr('latest.EPS.tolist()[0]', latest, df),
        'rhs': eval_expr('df.EPS.iloc[[5]].tolist()[0]', latest, df),
        'lcol': 'EPS',
        'rcol': 'EPS 5 years ago'
    }, {
        'id': 'performance_check3',
        'rule': 'ROE is greater than 20%',
        'outcome': perform_operation('(latest.ROE * 100 > 20).tolist()[0]', latest, df, silent=silent),
        'lhs': eval_expr('(latest.ROE * 100).tolist()[0]', latest, df),
        'rhs': 20,
        'lcol': 'ROE',
        'rcol': None
    }, {
        'id': 'performance_check4',
        'rule': 'ROCE is greater than ROCE 3 years ago',
        'outcome': perform_operation('(latest.ROCE * 100).tolist()[0] > (df.ROCE * 100).iloc[[3]].tolist()[0]', latest, df, silent=silent),
        'lhs': eval_expr('(latest.ROCE * 100).tolist()[0]', latest, df),
        'rhs': eval_expr('(df.ROCE * 100).iloc[[3]].tolist()[0]', latest, df),
        'lcol': 'ROCE',
        'rcol': 'ROCE 3 years ago'
    }, {
        'id': 'performance_check5',
        'rule': 'ROA is greater than 10%',
        'outcome': perform_operation('(latest.ROA * 100 > 10).tolist()[0]', latest, df, silent=silent),
        'lhs': eval_expr('(latest.ROA * 100).tolist()[0]', latest, df),
        'rhs': 10,
        'lcol': 'ROA',
        'rcol': None
    }, {
        'id': 'performance_check6',
        'rule': 'ROA > 5 year average ROA',
        'outcome': perform_operation('(latest.ROA > df.head(5).ROA.mean()).tolist()[0]', latest, df, silent=silent),
        'lhs': eval_expr('latest.ROA.tolist()[0] * 100', latest, df),
        'rhs': eval_expr('df.head(5).ROA.mean() * 100', latest, df),
        'lcol': 'ROA',
        'rcol': 'ROA 5 year avg.'
    }, {
        'id': 'performance_check7',
        'rule': 'CROCI > 3 year average CROCI',
        'outcome': perform_operation('(latest.CROCI > df.head(3).CROCI.mean()).tolist()[0]', latest, df, silent=silent),
        'lhs': eval_expr('latest.CROCI.tolist()[0] * 100', latest, df),
        'rhs': eval_expr('df.head(3).CROCI.mean() * 100', latest, df),
        'lcol': 'CROCI',
        'rcol': 'CROCI 3 year avg.'
    }, {
        'id': 'performance_check8',
        'rule': 'Net Profit Margin > 3 year average Net Profit Margin',
        'outcome': perform_operation('(latest.NETPCT > df.head(3).NETPCT.mean()).tolist()[0]', latest, df, silent=silent),
        'lhs': eval_expr('latest.NETPCT.tolist()[0] * 100', latest, df),
        'rhs': eval_expr('df.head(3).NETPCT.mean() * 100', latest, df),
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


def perform_operation(expression, latest, df, silent=False):
        try:
            ret = eval(expression)
        except Exception as e:
            if not silent:
                print(f"Exception while evaluating expression: ${expression}. Exception is ${e}")
            ret = False

        return ret


def eval_expr(expression, latest, df, silent=True):
    try:
        ret = eval(expression)
    except Exception as e:
        if not silent:
            print(f"Exception while evaluating expression: ${expression}. Exception is ${e}")
        ret = "N/A"

    return ret


def perform_momentum_checks(df, silent=False):
    df = df.sort_index(ascending=False)
    latest = get_latest_non_zero(df, [
        'roc30',
        'roc60',
        'hhv52',
        'hhv_all_time',
        'close'
    ])

    checks = [{
        'id': 'mom_check1',
        'rule': 'ROC 30 >= 30',
        'outcome': perform_operation('(latest.roc30 >= 30).tolist()[0]', latest, df, silent=silent),
        'lhs': eval_expr('latest.roc30.tolist()[0]', latest, df),
        'rhs': 30,
        'lcol': 'ROC 30',
        'rcol': None
    }, {
        'id': 'mom_check2',
        'rule': 'ROC 60 > 30 & ROC 60 < 100',
        'outcome': perform_operation('(latest.roc60 < 100).tolist()[0] and (latest.roc60 > 30).tolist()[0]',
                                     latest,
                                     df,
                                     silent=silent),
        'lhs': eval_expr('latest.roc60.tolist()[0]', latest, df),
        'rhs': 100,
        'lcol': 'ROC 60',
        'rcol': None
    }, {
        'id': 'mom_check3',
        'rule': 'Current Price with 10% of HHV 52',
        'outcome': perform_operation('latest.close.tolist()[0] >= (latest.hhv52.tolist()[0] * .9)', latest, df, silent=silent),
        'lhs': eval_expr('latest.close.tolist()[0]', latest, df),
        'rhs': eval_expr('(latest.hhv52.tolist()[0])', latest, df),
        'lcol': 'Current Price',
        'rcol': 'HHV 52'
    },
        {
            'id': 'mom_check4',
            'rule': 'Current Price with 10% of All time high(4 years)',
            'outcome': perform_operation('latest.close.tolist()[0] >= (latest.hhv_all_time.tolist()[0] * .9)', latest, df,
                                         silent=silent),
            'lhs': eval_expr('latest.close.tolist()[0]', latest, df),
            'rhs': eval_expr('(latest.hhv_all_time.tolist()[0])', latest, df),
            'lcol': 'Current Price',
            'rcol': 'HHV All time'
        }
    ]

    return checks



def perform_health_checks(df, silent=False):
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
        'outcome': perform_operation('(latest.CRATIO > 1).tolist()[0]', latest, df, silent=silent),
        'lhs': eval_expr('latest.CRATIO.tolist()[0]', latest, df),
        'rhs': 1,
        'lcol': 'Current Ratio',
        'rcol': None
    }, {
        'id': 'health_check2',
        'rule': 'Solvency Ratio > .2',
        'outcome': perform_operation('(latest.SOLRATIO > .2).tolist()[0]', latest, df, silent=silent),
        'lhs': eval_expr('latest.SOLRATIO.tolist()[0]', latest, df),
        'rhs': .2,
        'lcol': 'Solvency Ratio',
        'rcol': None
    }, {
        'id': 'health_check3',
        'rule': 'Solvency ratio is greater than Solvency ratio 3 years ago',
        'outcome': perform_operation('(latest.SOLRATIO).tolist()[0] > (df.SOLRATIO).iloc[[3]].tolist()[0]', latest, df, silent=silent),
        'lhs': eval_expr('(latest.SOLRATIO).tolist()[0]', latest, df),
        'rhs': eval_expr('(df.SOLRATIO).iloc[[3]].tolist()[0]', latest, df),
        'lcol': 'Solvency Ratio',
        'rcol': 'Solvency Ratio 3 years ago'
    }, {
        'id': 'health_check4',
        'rule': 'Debt to equity is less than Debt to equity 5 years ago',
        'outcome': perform_operation('(latest.LTDE).tolist()[0] < (df.LTDE).iloc[[5]].tolist()[0]', latest, df, silent=silent),
        'lhs': eval_expr('(latest.LTDE).tolist()[0]', latest, df),
        'rhs': eval_expr('(df.LTDE).iloc[[5]].tolist()[0]', latest, df),
        'lcol': 'Debt to Equity',
        'rcol': 'DE 5 years ago'
    }, {
        'id': 'health_check5',
        'rule': 'Debt to Equity < 1',
        'outcome': perform_operation('(latest.LTDE < 1).tolist()[0]', latest, df, silent=silent),
        'lhs': eval_expr('latest.LTDE.tolist()[0]', latest, df),
        'rhs': 1,
        'lcol': 'Debt to Equity',
        'rcol': None
    }, {
        'id': 'health_check6',
        'rule': 'Interest Coverage > 5',
        'outcome': perform_operation('(latest.IC > 5).tolist()[0]', latest, df, silent=silent),
        'lhs': eval_expr('latest.IC.tolist()[0]', latest, df),
        'rhs': 5,
        'lcol': 'Interest Coverage',
        'rcol': None
    }, {
        'id': 'health_check7',
        'rule': 'Debt to Assets < .7',
        'outcome': perform_operation('(latest.DEBT_ASSETS < .7).tolist()[0]', latest, df, silent=silent),
        'lhs': eval_expr('latest.DEBT_ASSETS.tolist()[0]', latest, df),
        'rhs': .7,
        'lcol': 'Debt to Assets',
        'rcol': None
    }, {
        'id': 'health_check8',
        'rule': 'Cash from operations 3 year average > Net profit 3 year average',
        'outcome': perform_operation('(df.CFO.head(3).mean() > df.NP.head(3).mean()).item()', latest, df, silent=silent),
        'lhs': eval_expr('df.CFO.head(3).mean()', latest, df),
        'rhs': eval_expr('df.NP.head(3).mean()', latest, df),
        'lcol': 'CFO 3 years avg.',
        'rcol': 'Net Profit 3 years avg.'
    }
    ]
    return checks


def perform_dividend_checks(df, silent=False):
    df = df.sort_index(ascending=False)
    latest = get_latest_non_zero(df, ['DIV', 'DIVPAY', 'DIVYLD'])

    checks = [{
        'id': 'div_check1',
        'rule': 'Dividend yield > 3%',
        'outcome': perform_operation('(latest.DIVYLD > .03).tolist()[0]', latest, df, silent=silent),
        'lhs': eval_expr('latest.DIVYLD.tolist()[0] * 100', latest, df),
        'rhs': .03 * 100,
        'lcol': 'Dividend Yield',
        'rcol': None
    }, {
        'id': 'div_check2',
        'rule': 'Latest dividend increased more than 25% since 3 years ago',
        'outcome': perform_operation('(latest.DIV).tolist()[0] * .75 > (df.DIV).iloc[[3]].tolist()[0]', latest, df, silent=silent),
        'lhs': eval_expr('(latest.DIV).tolist()[0]', latest, df),
        'rhs': eval_expr('(df.DIV).iloc[[3]].tolist()[0]', latest, df),
        'lcol': 'Dividend',
        'rcol': 'Dividend 3 years ago'
    }, {
        'id': 'div_check3',
        'rule': 'Latest dividend increased more than 50% since 6 years ago',
        'outcome': perform_operation('(latest.DIV).tolist()[0] * .5 > (df.DIV).iloc[[6]].tolist()[0]', latest, df, silent=silent),
        'lhs': eval_expr('(latest.DIV).tolist()[0]', latest, df),
        'rhs': eval_expr('(df.DIV).iloc[[6]].tolist()[0]', latest, df),
        'lcol': 'Dividend',
        'rcol': 'Dividend 6 years ago'
    }, {
        'id': 'div_check4',
        'rule': 'Dividend payout between 10% and 60%',
        'outcome': perform_operation('(latest.DIVPAY > .1).tolist()[0] and (latest.DIVPAY < .6).tolist()[0]', latest, df, silent=silent),
        'lhs': eval_expr('latest.DIVPAY.tolist()[0] * 100', latest, df),
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


def analyse(company_name, company_dataframe=None, silent=False, score_only=False):
    if not company_dataframe:
        company_dataframe = DataAccess.get_company_dataframe(company_name)

    return {
        'consolidated': analyse_company(company_name, company_dataframe, 'consolidated', silent=silent, score_only=score_only),
        'standalone': analyse_company(company_name, company_dataframe, 'standalone',silent=silent, score_only=score_only)
    }


def analyse_company(company_name, company_dataframe=None, data_type='standalone', silent=False, score_only=False):
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
        valuation_checks = perform_valuation_checks(df, silent=silent)
        score = get_score_from_checks(valuation_checks)
    except Exception as e:
        if not silent:
            print(f"[{company_name}]Exception during valuation checks. Exception: {e}")
    result['valuation'] = {}

    if not score_only:
        result['valuation']['checks'] = valuation_checks
    result['valuation']['score'] = score

    p_checks = None
    score = None
    try:
        p_checks = perform_performance_checks(df, silent=silent)
        score = get_score_from_checks(p_checks)
    except Exception as e:
        if not silent:
            print(f"[{company_name}]Exception during valuation checks. Exception: {e}")
    result['performance'] = {}

    if not score_only:
        result['performance']['checks'] = p_checks
    result['performance']['score'] = score

    h_checks = None
    score = None
    try:
        h_checks = perform_health_checks(df,silent=silent)
        score = get_score_from_checks(h_checks)
    except Exception as e:
        if not silent:
            print(f"[{company_name}]Exception during valuation checks. Exception: {e}")
    result['health'] = {}
    if not score_only:
        result['health']['checks'] = h_checks
    result['health']['score'] = score

    d_checks = None
    score = None
    try:
        d_checks = perform_dividend_checks(df, silent=silent)
        score = get_score_from_checks(d_checks)
    except Exception as e:
        if not silent:
            print(f"[{company_name}]Exception during valuation checks. Exception: {e}")
    result['dividends'] = {}
    if not score_only:
        result['dividends']['checks'] = d_checks
    result['dividends']['score'] = score

    m_checks = None
    score = None
    try:
        m_checks = perform_momentum_checks(DBUtil.get_technicals_as_df(company_name), silent=silent)
        score = get_score_from_checks(m_checks)
    except Exception as e:
        if not silent:
            print(f"[{company_name}]Exception during momentum checks. Exception: {e}")
    result['momentum'] = {}
    if not score_only:
        result['momentum']['checks'] = m_checks
    result['momentum']['score'] = score

    return result


def analysis_report(comp, app=None):
    with app.app_context():
        info = {}
        data = DataAccess.get_data(company_name=comp, indicators=['SR', 'OP', 'NP'])
        info['info'] = DBUtil.to_json(CompanyInfo.query.get(comp))
        info['data'] = data
        a_r = analyse(comp, score_only=True, silent=True)
        info['analysis'] = {
            'standalone': {
                'dividends': a_r['standalone']['dividends']['score'],
                'valuation': a_r['standalone']['valuation']['score'],
                'performance': a_r['standalone']['performance']['score'],
                'health': a_r['standalone']['health']['score'],
                'momentum': a_r['standalone']['momentum']['score']
            },
            'consolidated': {
                'dividends': a_r['consolidated']['dividends']['score'],
                'valuation': a_r['consolidated']['valuation']['score'],
                'performance': a_r['consolidated']['performance']['score'],
                'health': a_r['consolidated']['health']['score'],
                'momentum': a_r['consolidated']['momentum']['score']
            }
        }
        return info


def assign_ranks(df):
    df['dividends_rank'] = df.dividends.rank(ascending=False)
    df['health_rank'] = df.health.rank(ascending=False)
    df['performance_rank'] = df.performance.rank(ascending=False)
    df['valuation_rank'] = df.valuation.rank(ascending=False)
    df['momentum_rank'] = df.momentum.rank(ascending=False)


    length = len(df)
    df['Score'] = (length - df['dividends_rank']) + (length - df['health_rank']) + (length - df['performance_rank']) + (length - df['valuation_rank']) + (length - df['momentum_rank'])
    df = df.sort_values(by='Score', ascending=False)
    return df


def analyse_list(company_list, app=None):
    c_dict = {}
    error_list = []
    print(f"Analysing companies {company_list}. Total: {len(company_list)}")
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        # Start the load operations and mark each future with its URL
        future_score = {}
        for code in company_list:
            future_score.update({executor.submit(analysis_report, code, app): code})

        for future in concurrent.futures.as_completed(future_score):
            company = future_score[future]
            try:
                info = future.result()
                c_dict[company] = info
            except Exception as exc:
                print('%r generated an exception: %s' % (company, exc))
                error_list.append(company)

    scores_std = {}
    scores_con = {}
    for k, v in c_dict.items():
        scores_std[k] = v['analysis']['standalone']
        scores_con[k] = v['analysis']['consolidated']

    df_std = pd.DataFrame(scores_std).transpose()
    df_con = pd.DataFrame(scores_con).transpose()

    df1 = assign_ranks(df_std)
    df2 = assign_ranks(df_con)

    sort_order_std = df1.index.tolist()
    sort_order_con = df2.index.tolist()

    new_dict1 = df1.transpose().to_dict()
    new_dict2 = df2.transpose().to_dict()

    for k, v in c_dict.items():
        del c_dict[k]['analysis']
        c_dict[k]['analysis_standalone'] = new_dict1[k]
        c_dict[k]['analysis_consolidated'] = new_dict2[k]

    c_dict['sort_order_standalone'] = sort_order_std
    c_dict['sort_order_consolidated'] = sort_order_con

    return c_dict, error_list

