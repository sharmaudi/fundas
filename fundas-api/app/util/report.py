import pickle

import pandas as pd
import math

from app.util.PathResolver import resolve_data


def CAGR(first, last, periods):
    return (last / first) ** (1 / periods) - 1


def get_report(report_type="merged"):
    standalone_set = pd.read_csv(resolve_data('report_standalone.csv'), index_col=0).fillna(0)
    consolidated_set = pd.read_csv(resolve_data('report_consolidated.csv'), index_col=0).fillna(0)

    standalone_set = standalone_set.head(20)
    consolidated_set = consolidated_set.head(20)

    error = set([line.strip() for line in open(resolve_data("error_list.csv"), 'r')])

    print("ERROR = " + str(error))

    # union = standalone_set.union(consolidated_set)
    #
    # if report_type == "standalone":
    #     proper = standalone_set
    # elif report_type == "consolidated":
    #     proper = consolidated_set
    # else:
    #     proper = union
    #
    # watchlist = {
    #     "proper": proper,
    #     "error": error
    # }
    # return watchlist

    print(standalone_set.transpose().to_dict())

    print(consolidated_set.transpose().to_dict())

    response = {
        'standalone_list': standalone_set.index.tolist(),
        'consolidated_list': consolidated_set.index.tolist(),
        'standalone': standalone_set.transpose().to_dict(),
        'consolidated': consolidated_set.transpose().to_dict(),
        'error': error
    }

    return response


def get_portfolio_report(report_type="merged"):
    standalone_set = pd.read_csv(resolve_data('portfolio_standalone.csv'), index_col=0).fillna(0)
    consolidated_set = pd.read_csv(resolve_data('portfolio_consolidated.csv'), index_col=0).fillna(0)

    standalone_set = standalone_set.head(25)
    consolidated_set = consolidated_set.head(25)

    error = set([line.strip() for line in open(resolve_data("portfolio_errors.csv"), 'r')])

    print("ERROR = " + str(error))

    # union = standalone_set.union(consolidated_set)
    #
    # if report_type == "standalone":
    #     proper = standalone_set
    # elif report_type == "consolidated":
    #     proper = consolidated_set
    # else:
    #     proper = union
    #
    # watchlist = {
    #     "proper": proper,
    #     "error": error
    # }
    # return watchlist

    print(standalone_set.transpose().to_dict())

    print(consolidated_set.transpose().to_dict())

    response = {
        'standalone_list': standalone_set.index.tolist(),
        'consolidated_list': consolidated_set.index.tolist(),
        'standalone': standalone_set.transpose().to_dict(),
        'consolidated': consolidated_set.transpose().to_dict(),
        'error': error
    }

    return response


def get_equity_curve_df(eq):
    index = []
    data = []

    for row in eq:
        index.append(row['date'])
        data.append(row['equity'])
    eq_df = pd.DataFrame(data, index=index, columns=['Equity'])
    return eq_df


def ceiling(x):
    return math.ceil(x * 100.0) / 100.0


def get_portfolio_performance_report():
    with open(resolve_data('portfolio.pkl'), 'rb') as handle:
        portfolio = pickle.loads(handle.read())

    with open(resolve_data('portfolio_index1.pkl'), 'rb') as handle:
        portfolio_nf = pickle.loads(handle.read())

    with open(resolve_data('portfolio_index2.pkl'), 'rb') as handle:
        portfolio_jnf = pickle.loads(handle.read())

    report = {}

    eq = get_equity_curve_df(portfolio['equityCurve'])
    eq_pct = pd.DataFrame(eq.Equity.pct_change().cumsum() * 100).dropna()
    eq1 = get_equity_curve_df(portfolio_nf['equityCurve'])
    eq1_pct = pd.DataFrame(eq1.Equity.pct_change().cumsum() * 100).dropna()
    eq2 = get_equity_curve_df(portfolio_jnf['equityCurve'])
    eq2_pct = pd.DataFrame(eq2.Equity.pct_change().cumsum() * 100).dropna()
    min_eq1 = eq_pct.Equity.min()
    min_eq2 = eq1_pct.Equity.min()
    min_eq3 = eq2_pct.Equity.min()
    max_eq1 = eq_pct.Equity.max()
    max_eq2 = eq1_pct.Equity.max()
    max_eq3 = eq2_pct.Equity.max()

    max_eq = max(max_eq1, max_eq2, max_eq3)

    min_eq = min(min_eq1, min_eq2, min_eq3)

    report['equityCurve'] = eq_pct.reset_index().to_dict(orient='split')['data']
    report['equityCurveNF'] = eq1_pct.reset_index().to_dict(orient='split')['data']
    report['equityCurveJNF'] = eq2_pct.reset_index().to_dict(orient='split')['data']

    report['equityCurveMaxValue'] = max_eq
    report['equityCurveMinValue'] = min_eq



    openPositions = pd.DataFrame(portfolio['openPositions']).transpose()
    closedPositions = pd.DataFrame(portfolio['closedPositions'])

    profit = 0
    closedProfit = 0

    if not openPositions.empty:
        openPositions['profit'] = (openPositions.current_price * openPositions.quantity) - openPositions.amount
        report['openPositions'] = openPositions.reset_index().to_dict(orient='split')
        report['current_profit'] = openPositions.profit.sum()
        report['max_gainer'] = openPositions[openPositions.profit == openPositions.profit.max()].reset_index()[
            ['index', 'profit']].to_dict(orient='records')
        report['max_loser'] = openPositions[openPositions.profit == openPositions.profit.min()].reset_index()[
            ['index', 'profit']].to_dict(orient='records')

        holdings = openPositions
        holdings['profit'] = (holdings.current_price * holdings.quantity) - holdings.amount
        profit = holdings.profit.sum()

    if not closedPositions.empty:
        closedPositions.rename(columns={
            'buyDate': 'BuyDate',
            'date': 'SellDate',
            'symbol': 'Symbol',
            'profit': 'Profit',
            'quantity': 'Quantity',
            'buyPrice': 'BuyPrice',
            'sellPrice': 'SellPrice'
        },
            inplace=True)
        closedPositions = closedPositions[
            ['Symbol', 'BuyDate', 'SellDate', 'Quantity', 'BuyPrice', 'SellPrice', 'Profit']]
        report['closedPositions'] = closedPositions.to_dict(orient='split')

        report['closed_profit'] = closedPositions.Profit.sum()
        closedProfit = closedPositions.Profit.sum()

    totalProfit = profit + closedProfit

    pf_eq_curve = get_equity_curve_df(portfolio['equityCurve'])

    profitPercentage = pf_eq_curve.Equity.pct_change().cumsum() * 100

    max_dd_perc_s = pf_eq_curve.Equity.pct_change().cumsum() * 100
    max_dd_perc = max_dd_perc_s.min()

    ser = pf_eq_curve.Equity
    pf_eq_curve['max2here'] = pd.expanding_max(ser)
    pf_eq_curve['dd2here'] = ser - pf_eq_curve['max2here']
    pf_eq_curve['maxdd'] = pd.expanding_min(pf_eq_curve['dd2here'])
    max_dd = pf_eq_curve['maxdd'].min()
    td = pf_eq_curve.tail(1).index.tolist()[0] - pf_eq_curve.head(1).index.tolist()[0]
    td_years = td.days / 365
    cagr = CAGR(500000, portfolio['equity'], td_years)

    stats = {
        'profit': profit,
        'closedProfit': closedProfit,
        'totalProfit': totalProfit,
        'profitPercentage': ceiling(profitPercentage.tail(1).tolist()[0]),
        'maxDrawdown': ceiling(max_dd),
        'maxDrawdownPercentage': ceiling(max_dd_perc),
        'cagr': ceiling(cagr * 100)
    }

    report['stats'] = stats

    return report
