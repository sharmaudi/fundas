import concurrent
import concurrent.futures
import os.path
import pickle
from datetime import datetime

import numpy as np
import pandas as pd
import quandl as q
from dateutil.parser import parse

from app.util import DataAccess, DBUtil, Analyzer
from app.util.PathResolver import resolve_data

q_api_key = 'R27JMJXy2W-fLV6LX48P'

c_dict = {}

def get_data_array(c_set):
    arr = []
    if 'Data' in c_set:
        arr = c_set['Data']
    return arr

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
    if company not in c_dict:
        c_dict[company] = DBUtil.get_technicals_as_df(company)
    return c_dict[company]


def getMarketValue(date, openPositions, startDate, endDate, split_data=None):
    currentTotalValue = 0
    totalAmount = 0
    lastKnownPrice = {}
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
                index = pd.date_range(startDate, endDate).sort_values()
                df = df.sort_index().reindex(index, method='ffill')
                df = df.fillna(initialPrice)
                close = df.ix[date].close
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
            except Exception as ex:
                print(f"Exception while processing {comp} for date{date}: {ex}")
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
            comp = s
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
        if not transactions.empty:
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
    index_price_df = index_price_df.sort_index().reindex(index.sort_values(), method='ffill')
    index_initial_price = index_price_df.ix()[start_date]['close']
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


def execute(local_filename='/Users/Udit/Dropbox/Watchlist/tradebook.xlsx'):
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
            'symbol': symbol,
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

    portfolio = create_portfolio(500000, transactions_df, split_data=splits)

    closed_df = pd.DataFrame(portfolio['closedPositions'])

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

    company_list = [val for val in portfolio['openPositions'].keys()]

    Analyzer.analyse_list(company_list, 'portfolio', map_symbols=False)


if __name__ == "__main__":
    execute()
