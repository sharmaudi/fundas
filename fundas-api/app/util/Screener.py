import pandas as pd
# import numpy as np

import urllib
import json
import urllib.request
import urllib.parse
import traceback


class Screener:
    url_template = 'http://www.screener.in/api/company/{}/'
    consolidated_url = 'http://www.screener.in/api/company/{}/consolidated'
    industry_template = 'http://www.screener.in/api/company/{}/peers/?industry={}'

    company_data = ''
    company_data_standalone = ''
    industry_data = ''
    name = ''
    id = ''
    industry = ''
    nse_code = ''
    bse_code = ''

    def get_company(self, nse_code, standalone=False):
        if not standalone:
            consolidated = self.consolidated_url.format(nse_code)
            try:
                #print('Getting consolidated figures from url : {}'.format(consolidated))
                response = urllib.request.urlopen(consolidated)
            except:
                url = self.url_template.format(nse_code)
                print('Error while getting consolidated figures for company {}'.format(nse_code))
                #print('Getting standalone figures from url : {}'.format(url))
                response = urllib.request.urlopen(url)
        else:
            url = self.url_template.format(nse_code)
            #print('Getting standalone figures from url : {}'.format(url))
            response = urllib.request.urlopen(url)

        str_response = response.read().decode('utf-8')
        obj = json.loads(str_response)
        return obj

    def get_related(self, p_id, p_industry):
        i_url = self.industry_template.format(p_id, urllib.parse.quote_plus(p_industry))

        #print('Getting related companies from {}'.format(i_url))
        try:
            response = urllib.request.urlopen(i_url)
        except:
            print('Error while getting related companies from {}. Trying alternate url.'.format(i_url));
            new_id = self.company_data['warehouse_set']['id']
            i_url = self.industry_template.format(new_id, urllib.parse.quote_plus(p_industry))
            try:
                response = urllib.request.urlopen(i_url)
            except:
                print('Error while getting related companies from {}. No other url to try.'.format(i_url));

        str_response = response.read().decode('utf-8')
        obj = json.loads(str_response)
        return obj

    @staticmethod
    def _get_data_frame_(p_json):
        rows = list()
        my_dict = dict()
        for row in p_json:
            name = row[0]
            rows.append(name)
            data = {a: b for a, b in row[1].items()}
            my_dict.update({name: data})
        df = pd.DataFrame(my_dict)
        ar = df.transpose()
        ar = ar.reindex(rows)
        return ar

    def get_balance_sheet(self):
        return self._get_data_frame_(self.company_data['number_set']['balancesheet'])

    def get_annual_report(self):
        return self._get_data_frame_(self.company_data['number_set']['annual'])

    def get_cash_flow(self):
        return self._get_data_frame_(self.company_data['number_set']['cashflow'])

    def get_quarterly_report(self):
        return self._get_data_frame_(self.company_data['number_set']['quarters'])

    def get_related_report(self):
        cols = [self.industry_data['ratios'][a][1] for a in range(0, len(self.industry_data['ratios']))]
        cols.insert(0, 'Full Name')
        c_list = dict()
        for l in self.industry_data['results']:
            r = l[0].split('/')[2]
            c_list.update({r: l[1:]})
        df = pd.DataFrame(c_list)
        df = df.transpose()
        df.columns = cols
        return df

    def get_related_companies(self, only_nse=True):
        self.industry_data = self.get_related(self.id, self.industry)
        ret_list = list()
        for l in self.industry_data['results']:
            r = l[0].split('/')[2]
            if only_nse:
                try:
                    int(r)
                except:
                    ret_list.append(r)
            else:
                ret_list.append(r)

        company_id = self.company_data_standalone['warehouse_set']['id']
        industry = self.company_data_standalone['warehouse_set']['industry']
        if company_id and industry and company_id != self.id:
            industry_standalone_data = self.get_related(company_id, industry)
            for l in industry_standalone_data['results']:
                r = l[0].split('/')[2]
                if only_nse:
                    try:
                        int(r)
                    except:
                        if r not in ret_list:
                            ret_list.append(r)
                else:
                    if r not in ret_list:
                        ret_list.append(r)
        return ret_list

    def get_pe(self, standalone=False):
        if not standalone:
            pe = float(pd.Series(self.company_data['warehouse_set'])['price_to_earning'])
        else:
            pe = float(pd.Series(self.company_data_standalone['warehouse_set'])['price_to_earning'])
        return pe

    def get_book_value(self, standalone=False):
        if not standalone:
            pbv = float(pd.Series(self.company_data['warehouse_set'])['book_value'])
        else:
            pbv = float(pd.Series(self.company_data_standalone['warehouse_set'])['book_value'])
        return pbv

    def get_current_price(self, standalone=False):
        if not standalone:
            current_price = float(pd.Series(self.company_data['warehouse_set'])['current_price'])
        else:
            current_price = float(pd.Series(self.company_data_standalone['warehouse_set'])['current_price'])
        return current_price

    def get_stats(self):
        ser = pd.Series(self.company_data['warehouse_set'])
        return ser

    def __init__(self, code):
        try:
            self.company_data = self.get_company(code)
        except:
            print(f"[{code}]Error while getting consolidated data. Getting standalone.")

        try:
            self.company_data_standalone = self.get_company(code, standalone=True)
        except Exception as e:
            print(f"[{code}]Init Threw Exception:{e}")
            raise e
