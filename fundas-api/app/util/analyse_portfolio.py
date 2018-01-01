import concurrent
import concurrent.futures
import csv
import json
import os.path
import pickle
from datetime import datetime

import numpy as np
import pandas as pd
import quandl as q
import redis
from dateutil.parser import parse

from app.util.PathResolver import resolve_data

r_cache = redis.StrictRedis(host='localhost', port=6379, db=2)

priceDict = {}
lastKnownPrice = {}
q_api_key = 'R27JMJXy2W-fLV6LX48P'


def get_data_array(c_set):
    arr = []
    if 'Data' in c_set:
        arr = c_set['Data']
    return arr


def calculate_scores(json_response, industry_data, momentum_data, standalone=False):
    checklist = {}

    checklist['performance'] = []
    checklist['momentum'] = []
    checklist['health'] = []
    checklist['valuation'] = []
    checklist['dividends'] = []

    key = 'Consolidated'
    if standalone:
        key = 'Standalone'

    company_pe_set = json_response[key][0]
    company_pbv_set = json_response[key][1]
    company_peg_set = json_response[key][2]
    company_eps5_set = json_response[key][3]
    company_eps_set = json_response[key][4]
    company_roe_set = json_response[key][5]
    company_roce_set = json_response[key][6]
    company_roa_set = json_response[key][7]
    company_croci_set = json_response[key][8]
    company_netpct_set = json_response[key][9]
    company_cratio_set = json_response[key][10]
    company_solratio_set = json_response[key][11]
    company_ltde_set = json_response[key][12]
    company_ic_set = json_response[key][13]
    company_debt_assets_set = json_response[key][14]
    company_divyld_set = json_response[key][15]
    company_div_set = json_response[key][16]
    company_divpay_set = json_response[key][17]
    company_evebitda_set = json_response[key][18]
    company_np_set = json_response[key][19]
    company_cfo_set = json_response[key][20]
    company_op_set = json_response[key][21]
    company_sr_set = json_response[key][22]

    pe_array = get_data_array(company_pe_set)
    peg_array = company_peg_set['Data']
    pbv_array = company_pbv_set['Data']
    eps5_array = company_eps5_set['Data']
    eps_array = company_eps_set['Data']
    roe_array = company_roe_set['Data']
    roce_array = company_roce_set['Data']
    roa_array = company_roa_set['Data']
    croci_array = company_croci_set['Data']
    netpct_array = company_netpct_set['Data']
    cratio_array = company_cratio_set['Data']

    solratio_array = get_data_array(company_solratio_set)

    ltde_array = company_ltde_set['Data']
    ic_array = company_ic_set['Data']
    debt_assets_array = company_debt_assets_set['Data']
    divyld_array = company_divyld_set['Data']
    div_array = company_div_set['Data']
    divpay_array = company_divpay_set['Data']
    ev_array = company_evebitda_set['Data']
    np_array = company_np_set['Data']
    cfo_array = company_cfo_set['Data']
    op_array = company_op_set['Data']
    sr_array = company_sr_set['Data']

    latest_np = np_array[len(np_array) - 1]
    np_1 = np_array[len(np_array) - 2]
    np_2 = np_array[len(np_array) - 3]

    latest_sr = sr_array[len(sr_array) - 1]
    sr_1 = sr_array[len(sr_array) - 2]
    sr_2 = sr_array[len(sr_array) - 3]

    latest_op = op_array[len(op_array) - 1]
    op_1 = op_array[len(op_array) - 2]
    op_2 = op_array[len(op_array) - 3]

    cfo_greater_than_np = False
    for i in range(0, 2):
        cfo = cfo_array.pop()

        np = np_array.pop()
        if isinstance(np, int) or isinstance(np, float):
            np *= .8
        else:
            np = 0

        cfo_greater_than_np = cfo >= np

    latest_pe = pe_array[len(pe_array) - 1]
    latest_pbv = pbv_array[len(pbv_array) - 1]
    latest_peg = 0
    if peg_array:
        latest_peg = peg_array[len(peg_array) - 1]

    latest_eps5 = eps5_array[len(eps5_array) - 1]
    latest_eps = eps_array[len(eps_array) - 1]
    latest_roe = roe_array[len(roe_array) - 1]
    latest_roce = roce_array[len(roce_array) - 1]
    latest_roa = roa_array[len(roa_array) - 1]
    latest_croci = croci_array[len(croci_array) - 1]
    latest_netpct = netpct_array[len(netpct_array) - 1]
    latest_cratio = cratio_array[len(cratio_array) - 1]
    latest_solratio = 0

    if solratio_array:
        latest_solratio = solratio_array[len(solratio_array) - 1]

    latest_ltde = ltde_array[len(ltde_array) - 1]

    latest_ic = 0
    if ic_array:
        latest_ic = ic_array[len(ic_array) - 1]
    latest_debt_assets = debt_assets_array[len(debt_assets_array) - 1]
    latest_divyld = divyld_array[len(divyld_array) - 1]
    latest_div = div_array[len(div_array) - 1]
    latest_divpay = divpay_array[len(divpay_array) - 1]

    latest_ev = 0
    if ev_array:
        latest_ev = ev_array[len(ev_array) - 1]

    pe_5_yr_avg = company_pe_set['Mean_5_YR']
    pe_avg = company_pe_set['Mean']

    nifty_pe = industry_data['nifty_pe']
    industry_pe = industry_data['PE']['weighed_average']
    industry_pbv = industry_data['PBV']['weighed_average']
    industry_eps5 = industry_data['EPS5']['weighed_average']
    industry_croci = industry_data['CROCI']['weighed_average']
    industry_roa = industry_data['ROA']['weighed_average']
    industry_netpct = industry_data['NETPCT']['weighed_average']
    industry_divyld = industry_data['DIVYLD']['weighed_average']
    industry_ev = industry_data['EVEBIDTA']['weighed_average']

    mom_score = 0
    latest_price = momentum_data['Technicals']['Price'][len(momentum_data['Technicals']['Price']) - 1]
    high_52 = momentum_data['Technicals']['52WHigh']
    latest_momentum = momentum_data['Technicals']['Momentum'][len(momentum_data['Technicals']['Momentum']) - 1]
    latest_qtr_growth_rev = momentum_data['Standalone']['SR_G'][len(momentum_data['Standalone']['SR_G']) - 1]
    latest_qtr_growth_np = momentum_data['Standalone']['NP_G'][len(momentum_data['Standalone']['NP_G']) - 1]

    score = 0

    valuation_checks = []

    outcome = False

    if latest_pe < nifty_pe:
        score += 1
        outcome = True

    valuation_checks.append({
        'id': 'check1',
        'rule': 'PE Ratio < NIFTY PE',
        'outcome': outcome

    })

    outcome = False

    if latest_pe < industry_pe:
        score += 1
        outcome = True

    valuation_checks.append({
        'id': 'check2',
        'rule': 'PE Ratio < Industry PE',
        'outcome': outcome

    })

    outcome = False

    if latest_pe < pe_5_yr_avg:
        score += 1
        outcome = True

    valuation_checks.append({
        'id': 'check3',
        'rule': 'PE Ratio < 5 Year Average PE',
        'outcome': outcome
    })

    outcome = False

    if latest_pe < pe_avg:
        score += 1
        outcome = True

    valuation_checks.append({
        'id': 'check4',
        'rule': 'PE Ratio < All time Average PE',
        'outcome': outcome
    })

    outcome = False

    if latest_peg and 1 > latest_peg > 0:
        score += 1
        outcome = True

    valuation_checks.append({
        'id': 'check5',
        'rule': 'PEG Ratio is within 0 and 1',
        'outcome': outcome
    })

    outcome = False

    if latest_ev and industry_ev > latest_ev > 0:
        score += 1
        outcome = True

    valuation_checks.append({
        'id': 'check6',
        'rule': 'EV/EBITDA < Industry average',
        'outcome': outcome
    })

    outcome = False

    if latest_pbv < industry_pbv:
        score += 1
        outcome = True

    valuation_checks.append({
        'id': 'check7',
        'rule': 'PB Ratio < Industry PB Ratio',
        'outcome': outcome
    })

    outcome = False

    perf_score = 0
    perf_checks = []

    if latest_eps5 > industry_eps5:
        perf_score += 1
        outcome = True

    perf_checks.append({
        'id': 'check1',
        'rule': '',
        'outcome': outcome
    })

    outcome = False

    if latest_eps > eps_array[len(eps_array) - 6]:
        perf_score += 1
        outcome = True

    perf_checks.append({
        'id': 'check2',
        'rule': '',
        'outcome': outcome
    })

    outcome = False

    if latest_roe >= .2:
        perf_score += 1
        outcome = True

    perf_checks.append({
        'id': 'check3',
        'rule': '',
        'outcome': outcome
    })

    outcome = False

    if latest_roce > roce_array[len(roce_array) - 4]:
        perf_score += 1
        outcome = True

    perf_checks.append({
        'id': 'check4',
        'rule': '',
        'outcome': outcome
    })

    outcome = False

    if latest_roa >= industry_roa:
        perf_score += 1
        outcome = True

    perf_checks.append({
        'id': 'check5',
        'rule': '',
        'outcome': outcome
    })

    outcome = False

    if latest_croci >= industry_croci:
        perf_score += 1
        outcome = True

    perf_checks.append({
        'id': 'check6',
        'rule': '',
        'outcome': outcome
    })

    outcome = False

    if latest_netpct >= industry_netpct:
        perf_score += 1
        outcome = True

    perf_checks.append({
        'id': 'check7',
        'rule': '',
        'outcome': outcome
    })
    outcome = False

    if latest_qtr_growth_np > 0:
        perf_score += 1
        outcome = True

    perf_checks.append({
        'id': 'check9',
        'rule': '',
        'outcome': outcome
    })

    outcome = False

    if latest_np > 0 and np_1 > 0 and 0 < np_2 < latest_np and latest_op > 0 and op_1 > 0 \
            and 0 < op_2 < latest_op and latest_sr > 0 and sr_1 > 0 and 0 < sr_2 < latest_sr:
        perf_score += 1
        outcome = True

    perf_checks.append({
        'id': 'check10',
        'rule': '',
        'outcome': outcome
    })

    health_score = 0

    health_checks = []

    outcome = False

    if latest_cratio > 1:
        health_score += 1
        outcome = True

    health_checks.append({
        'id': 'check1',
        'rule': '',
        'outcome': outcome
    })

    outcome = False

    if solratio_array and latest_solratio > .2:
        health_score += 1
        outcome = True

    health_checks.append({
        'id': 'check2',
        'rule': '',
        'outcome': outcome
    })

    outcome = False

    if solratio_array:
        if latest_solratio >= solratio_array[len(solratio_array) - 4]:
            health_score += 1
            outcome = True

    health_checks.append({
        'id': 'check3',
        'rule': '',
        'outcome': outcome
    })

    outcome = False

    if latest_ltde <= ltde_array[len(ltde_array) - 6]:
        health_score += 1
        outcome = True

    health_checks.append({
        'id': 'check4',
        'rule': '',
        'outcome': outcome
    })

    outcome = False

    if latest_ltde < 1:
        health_score += 1
        outcome = True

    health_checks.append({
        'id': 'check5',
        'rule': '',
        'outcome': outcome
    })

    outcome = False

    if latest_ic > 5:
        health_score += 1
        outcome = True

    health_checks.append({
        'id': 'check6',
        'rule': '',
        'outcome': outcome
    })

    outcome = False

    if latest_debt_assets < .7:
        health_score += 1
        outcome = True

    health_checks.append({
        'id': 'check7',
        'rule': '',
        'outcome': outcome
    })

    outcome = False

    if cfo_greater_than_np:
        health_score += 1
        outcome = True

    health_checks.append({
        'id': 'check8',
        'rule': '',
        'outcome': outcome
    })

    outcome = False

    div_score = 0
    div_checks = []

    if latest_divyld >= .03:
        div_score += 1
        outcome = True

    div_checks.append({
        'id': 'check1',
        'rule': '',
        'outcome': outcome
    })

    outcome = False
    if latest_divyld > industry_divyld:
        div_score += 1
        outcome = True

    div_checks.append({
        'id': 'check2',
        'rule': '',
        'outcome': outcome
    })
    outcome = False
    if latest_div > div_array[len(div_array) - 2] * .75:
        div_score += 1
        outcome = True

    div_checks.append({
        'id': 'check3',
        'rule': '',
        'outcome': outcome
    })
    outcome = False
    if latest_div > div_array[len(div_array) - 6]:
        div_score += 1
        outcome = True

    div_checks.append({
        'id': 'check4',
        'rule': '',
        'outcome': outcome
    })
    outcome = False
    if .1 < latest_divpay < .9:
        div_score += 1
        outcome = True

    div_checks.append({
        'id': 'check5',
        'rule': '',
        'outcome': outcome
    })
    outcome = False

    mom_checks = []

    if latest_momentum >= 30:
        mom_score += 1
        outcome = True

    mom_checks.append({
        'id': 'check1',
        'rule': '',
        'outcome': outcome
    })
    outcome = False
    if latest_price >= (high_52 * .8):
        mom_score += 1
        outcome = True

    mom_checks.append({
        'id': 'check2',
        'rule': '',
        'outcome': outcome
    })

    perf_score = round(10 / 9 * perf_score)

    if perf_score > 10:
        perf_score = 10

    mom_score = round(10 / 2 * mom_score)
    div_score = round(10 / 5 * div_score)
    health_score = round(10 / 8 * health_score)
    score = round(10 / 7 * score)

    return {
        'performance': perf_score,
        'momentum': mom_score,
        'dividends': div_score,
        'health': health_score,
        'valuation_checklist': valuation_checks,
        'performance_checklist': perf_checks,
        'health_checklist': health_checks,
        'dividends_checklist': div_checks,
        'momentum_checklist': mom_checks,
        'valuation': score
    }


# noinspection PyBroadException
def get_scores(company):
    key_prefix = "analysis_"

    key = key_prefix + company

    ttl = r_cache.ttl(key)

    if ttl == -1:
        print("Cache Entry for {} has expired. Recreating")
        r_cache.delete(key)

    data = r_cache.get(key)
    if data:
        data = data.decode('UTF-8')
        print("Screener Cache hit for " + key)
        return json.loads(data)
    else:
        print("No Cache Entry found for {}. Getting from api".format(key))

    indicators = 'PE,PBV,PEG,EPS5,EPS,ROE,ROCE,ROA,CROCI,NETPCT,CRATIO,SOLRATIO,LTDE,IC,DEBT_ASSETS,DIVYLD,DIV,DIVPAY,EVEBIDTA,NP,CFO,SR,OP'
    indicator_list = indicators.split(',')
    def_score = {
        'performance': 0,
        'momentum': 0,
        'dividends': 0,
        'health': 0,
        'valuation': 0
    }
    c_score = def_score
    s_score = def_score

    dataIsGood = True
    try:
        jsonResponse = DataAccess.get_data(company, indicator_list, get_quarterly=False)
        industry_data = DataAccess.get_industry_data(company, use_screener=False)
        momentumData = DataAccess.get_technicals(company)
    except:
        print("Exception while getting data for company {}".format(company))
        dataIsGood = False

    c_error = False
    s_error = False

    if (dataIsGood):
        try:
            c_score = calculate_scores(jsonResponse, industry_data, momentumData)
            c_score['error'] = False
        except:
            c_error = True
            c_score['error'] = True
            print("Exception while calculating consolidated scores for company : {}".format(company))

        try:
            s_score = calculate_scores(jsonResponse, industry_data, momentumData, standalone=True)
            s_score['error'] = False
        except:
            s_error = True
            s_score['error'] = True
            print("Exception while calculating standalone scores for company : {}".format(company))

        if c_error and s_error:
            print("Not able to analyse {}. Check manually.".format(company))
    else:
        return {
            'consolidated': {},
            'standalone': {},
            'error': True
        }

    ret_obj = {
        'consolidated': c_score,
        'standalone': s_score,
        'error': c_error and s_error
    }

    r_cache.set(key, json.dumps(ret_obj))
    r_cache.expire(key, 7 * 24 * 60 * 60)

    return ret_obj


def assign_ranks(df):
    df['dividends_rank'] = df.dividends.rank(ascending=True)
    df['health_rank'] = df.health.rank(ascending=True)
    df['momentum_rank'] = df.momentum.rank(ascending=True)
    df['performance_rank'] = df.performance.rank(ascending=True)
    df['valuation_rank'] = df.valuation.rank(ascending=True)
    df['Score'] = df['dividends_rank'] + df['health_rank'] + df['momentum_rank'] + df['performance_rank'] + df[
        'valuation_rank']
    df = df.sort_values(by='Score', ascending=False)
    return df


def getCompanyName(key):
    if key.lower().startswith('nse:'):
        comp = key.split(':')[1]
    elif key.lower().endswith('.ns'):
        comp = key.split('.')[0]
    else:
        comp = key
    return comp


def max_drawdown(ser):
    max2here = pd.expanding_max(ser)
    dd2here = ser - max2here
    return dd2here.min()


def parse_date(dateStr):
    print('Parsing date : {}'.format(dateStr))
    return parse(dateStr).date()


def getPrices(company, force=False):
    fname = 'data/' + company + '.csv'
    df = pd.DataFrame()
    if not force and os.path.isfile(fname):
        df = pd.read_csv(fname, index_col=0, parse_dates=True)
    if df.empty:
        print('Dataframe not found in csv. Getting from Quandl')
        key = 'NSE/{}'.format(company)
        df = q.get(key, authtoken=q_api_key, returns='pandas', collapse='daily', trim_start='01-01-12')
        df.to_csv('data/' + company + ".csv")
    priceDict.update({company: df})
    return df


def getMarketValue(date, openPositions, startDate, endDate, split_data=None):
    currentTotalValue = 0
    totalAmount = 0
    for key in openPositions.keys():
        if key.lower().startswith('nse:'):
            comp = key.split(':')[1]
        elif key.lower().endswith('.ns'):
            comp = key.split('.')[0]
        else:
            comp = key
        position = openPositions[key]
        amount = position['amount']
        quantity = position['quantity']
        initialPrice = amount / quantity
        df = getPrices(comp)
        close = initialPrice

        if not df.empty:
            try:
                index = pd.date_range(startDate, endDate)
                df = df.reindex(index, method='ffill')
                df = df.fillna(initialPrice)
                close = df.ix[date].Close
                if close == np.nan:
                    print('Closing Price not found for {} on date {}. Returning last known price'.format(comp, date))
                    if comp in lastKnownPrice.keys():
                        close = lastKnownPrice[comp]
                    else:
                        close = initialPrice
                else:
                    lastKnownPrice.update({comp: close})


            except KeyError:
                print('KEYERROR!!Closing Price not found for {} on date {}. Returning last known price'.format(comp,
                                                                                                               date))
                if comp in lastKnownPrice.keys():
                    close = lastKnownPrice[comp]
                else:
                    close = initialPrice
        else:
            print('Closing prices not found for : {}'.format(comp))

        currentValue = quantity * close
        currentProfit = currentValue - amount
        currentTotalValue = currentTotalValue + currentValue
        openPositions[key].update({'current_price': close})
        totalAmount = totalAmount + amount
    # print('close prices for {} on date {} : {}. Current profit is {}. Quantity:{}. Original Amount:{}'.format(comp,date,close,currentProfit,quantity,amount))

    #    print('Portfolio profit on {} is {}'.format(date,(currentTotalValue - totalAmount)))
    return currentTotalValue


def refreshPricesAsync(c_list, i_list=['NIFTYBEES', 'JUNIORBEES']):
    c_list.extend(i_list)
    print(c_list)
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:

        future_to_url = {}
        for c in c_list:
            company = getCompanyName(c)
            print("Company : {}".format(company))
            future_to_url.update({executor.submit(getPrices, company, True): c})

        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (url, exc))
            else:
                print('%r page is %d bytes' % (url, len(data)))


def create_portfolio(initialEquity, transactions_df, split_data=None):
    dates = transactions_df.date.values.tolist()
    startDate = dates[0]
    #    endDate = dates[-1]
    endDate = datetime.today().replace(tzinfo=None)
    portfolio = {
        'openPositions': {},
        'marketValue': 0,
        'equity': 0,
        'cash': 0,
        'closedPositions': [],
        'equityCurve': []
    }

    initialEquity = initialEquity

    portfolio['cash'] = initialEquity
    portfolio['equity'] = initialEquity

    for date in pd.date_range(start=startDate, end=endDate):
        for s in portfolio['openPositions']:
            comp = s.split(':')[1]
            if comp in split_data:
                split_date = datetime.strptime(split_data[comp][1], "%d-%m-%Y")
                if date == split_date:
                    print('Split found for company : ' + comp)
                    print('Date : {}, Split Date: {}'.format(date, split_date))
                    q = portfolio['openPositions'][s]['quantity'] * split_data[comp][0]
                    portfolio['openPositions'].update({s: {
                        'quantity': q,
                        'amount': portfolio['openPositions'][s]['amount'],
                        'buyDate': date.date(),
                        'average_price': portfolio['openPositions'][s]['amount'] / q
                    }})
        transactions = transactions_df[transactions_df.date == date.date()]
        portfolio['date'] = date.date()
        if transactions.empty:
            print("Date : {}, No Tranactions".format(date.date()))
        else:
            count = len(transactions.index.tolist())
            print("Date : {}, Transactions : {}".format(date.date(), count))
            for row in transactions.iterrows():
                if row[1].typeCode == 'DEPOSIT':
                    # Ignore deposits
                    print("Type : {}, Amount : {}".format(row[1].typeCode, row[1].amount))
                if row[1].typeCode == 'BUY':
                    quantity = abs(row[1].quantity)
                    amount = abs(row[1].amount)
                    symbol = row[1].symbol
                    openPositions = portfolio['openPositions']
                    if symbol in openPositions:
                        position = openPositions[symbol]
                        position['quantity'] = position['quantity'] + quantity
                        position['amount'] = position['amount'] + amount
                        position['average_price'] = position['amount'] / position['quantity']
                    else:
                        portfolio['openPositions'].update({symbol: {
                            'quantity': quantity,
                            'amount': amount,
                            'buyDate': date.date(),
                            'average_price': amount / quantity
                        }})
                    portfolio['cash'] = portfolio['cash'] - amount
                if row[1].typeCode == 'SELL':
                    symbol = row[1].symbol
                    quantity = abs(row[1].quantity)
                    amount = abs(row[1].amount)

                    if symbol in openPositions:
                        position = openPositions[symbol]
                        initialQuantity = position['quantity']
                        initialAmount = position['amount']
                        changeInPosition = initialQuantity - quantity
                        profit = amount - initialAmount
                        currentPPS = amount / quantity
                        initialPPS = initialAmount / initialQuantity
                        print('Symbol : {}, Initial Quantity : {}, Sell Quantity : {}'.format(symbol, initialQuantity,
                                                                                              quantity))


                        if (changeInPosition == 0):
                            profit = amount - initialAmount
                            print('Position closed in {}, profit : {}'.format(symbol, profit))
                            portfolio['closedPositions'].append({
                                'date': date.date(),
                                'symbol': symbol,
                                'quantity': quantity,
                                'profit': profit,
                                'buyPrice': initialPPS,
                                'sellPrice': currentPPS,
                                'buyDate': position['buyDate']
                            })
                            del openPositions[symbol]
                        else:
                            partialProfit = (amount - (quantity * initialPPS))
                            position['quantity'] = changeInPosition
                            position['amount'] = initialAmount - (quantity * initialPPS)
                            portfolio['closedPositions'].append({
                                'date': date.date(),
                                'symbol': symbol,
                                'quantity': quantity,
                                'profit': partialProfit,
                                'buyPrice': initialPPS,
                                'sellPrice': currentPPS,
                                'buyDate': position['buyDate']
                            })
                            print('Scaled out in {}'.format(symbol))
                            print('Partial Profit : {}'.format(partialProfit))


                        portfolio['cash'] = portfolio['cash'] + amount
                    else:
                        print('No Buy Entry found for {}'.format(symbol))

        portfolio['marketValue'] = getMarketValue(date, portfolio['openPositions'], startDate, endDate,
                                                  split_data=split_data)
        portfolio['equity'] = portfolio['cash'] + portfolio['marketValue']
        equityCurve = portfolio['equityCurve']
        equityCurve.append({'date': date, 'equity': portfolio['equity']})

    return portfolio


def get_equity_curve_df(eq):
    index = []
    data = []

    for row in eq:
        index.append(row['date'])
        data.append(row['equity'])
    eq_df = pd.DataFrame(data, index=index, columns=['Equity'])
    return eq_df


def get_index_df(start_date, name):
    end_date = datetime.now()
    index_price_df = getPrices(name)
    index = pd.date_range(start_date, end_date)
    index_price_df = index_price_df.reindex(index, method='ffill')
    index_initial_price = index_price_df.ix()[start_date]['Close']
    quantity = 300000 / index_initial_price
    index_dict = {
        'date': start_date,
        'orderNumber': '11112222',
        'symbol': 'NSE:{}'.format(name),
        'typeCode': 'BUY',
        'quantity': quantity,
        'amount': index_initial_price * quantity,
        'pricePerShare': index_initial_price

    }
    index_df1 = pd.DataFrame([index_dict])
    index_df1.set_index(['date'])
    return index_df1

def execute():
    local_filename = '/Dropbox/tradebook.xlsx'
    skip_row = 11
    cols = 'B:J'
    splits = {'SUNILHITEC': [20, '01-12-2016'],
              'POLYMED': [2, '24-03-2017'],
              'JAMNAAUTO': [5, '05-10-2017']
              }
    df = pd.read_excel(local_filename, sheetname=0, parse_cols=cols, skiprows=skip_row)
    print("Tradebook: ".format(df))
    for i in df.Symbol.tolist():
        if i in splits:
            print('{} --> {}:1'.format(i, str(splits[i][0])))
            df.ix[df.Symbol == i, 'Qty'] = df.ix[df.Symbol == i, 'Qty']
            df.ix[df.Symbol == i, 'Rate'] = df.ix[df.Symbol == i, 'Rate']
            df.ix[df.Symbol == i, 'Split'] = '{}:1'.format(splits[i][0])
    transactions_list = []
    index_list = []
    for index, row in df.iterrows():
        n = index
        date = row['Trade date']
        time = row['Trade time']
        exchange = row['Exchange']
        symbol = row['Symbol']
        oper = row['Type']
        qty = row['Qty']
        rate = row['Rate']
        split = row['Split']
        orderNumber = row['Order no']

        dateTimeStr = str(date)

        print(dateTimeStr)

        typeCode = 'BUY'
        if oper == 'S':
            typeCode = 'SELL'

        row = {
            'date': datetime.strptime(dateTimeStr, '%d-%m-%Y').replace(tzinfo=None).date(),
            'typeCode': typeCode,
            'symbol': exchange + ":" + symbol,
            'quantity': qty,
            'pricePerShare': rate,
            'amount': float(qty) * float(rate),
            'orderNumber': orderNumber
        }
        transactions_list.append(row)
        index_list.append(index)

    # Combine order numbers
    transactions_df = pd.DataFrame(transactions_list, index=index_list)
    group = transactions_df.groupby(['date', 'orderNumber', 'symbol', 'typeCode'])
    aggregations = {
        'quantity': 'sum',
        'pricePerShare': 'mean',
        'amount': 'sum',
    }

    transactions_df = group.agg(aggregations).reset_index()
    print(transactions_df)

    refreshPricesAsync(transactions_df.symbol.tolist())

    portfolio = create_portfolio(500000, transactions_df, split_data=splits)

    closed_df = pd.DataFrame(portfolio['closedPositions'])

    print('Total Profit/Loss on Closed Trades= {}'.format(closed_df.profit.sum()))

    print('Portfolio: {}'.format(portfolio))

    start_date = transactions_df.date[0]

    index_df1 = get_index_df(start_date, 'NIFTYBEES')
    index_df2 = get_index_df(start_date, 'JUNIORBEES')

    portfolio_index1 = create_portfolio(500000, index_df1, split_data={})
    portfolio_index2 = create_portfolio(500000, index_df2, split_data={})

    with open(resolve_data("portfolio.pkl"), 'wb') as f:
        pickle.dump(portfolio, f, pickle.HIGHEST_PROTOCOL)

    with open(resolve_data("portfolio_index1.pkl"), 'wb') as f:
        pickle.dump(portfolio_index1, f, pickle.HIGHEST_PROTOCOL)

    with open(resolve_data("portfolio_index2.pkl"), 'wb') as f:
        pickle.dump(portfolio_index2, f, pickle.HIGHEST_PROTOCOL)

    company_list = [val.split(":")[1] for val in portfolio['openPositions'].keys()]

    c_score_dict = {}
    s_score_dict = {}
    error_list = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # Start the load operations and mark each future with its URL

        future_score = {}

        for comp in company_list:
            future_score.update({executor.submit(get_scores, comp): comp})

        for future in concurrent.futures.as_completed(future_score):
            company = future_score[future]
            try:
                scores = future.result()
                print('-' * 100)
                print('Company - {}'.format(company))
                print(scores)
                print('-' * 100)
                c_score_dict.update({company: scores['consolidated']})
                s_score_dict.update({company: scores['standalone']})
                if scores['error']:
                    error_list.append(company)
            except Exception as exc:
                print('%r generated an exception: %s' % (company, exc))

    df_c = pd.DataFrame(c_score_dict).transpose()
    df_s = pd.DataFrame(s_score_dict).transpose()

    df_c = assign_ranks(df_c)
    df_s = assign_ranks(df_s)


    df_s.to_csv(resolve_data("portfolio_standalone.csv"))
    df_c.to_csv(resolve_data("portfolio_consolidated.csv"))

    print('*' * 100)
    print("Following companies have errors. Analyse Manually: {}".format(error_list))

    with open(resolve_data("portfolio_error_list.csv"), "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        for val in error_list:
            writer.writerow([val])


if __name__ == "__main__":
    execute()