import pandas as pd
import csv
import concurrent.futures
import urllib.request
import json


import redis

from app.util import Analyzer, DataAccess
from app.util.PathResolver import resolve_data

r_cache = redis.StrictRedis(host='redis', port=6379, db=2)


def assign_ranks(df):
    df['dividends_rank'] = df.dividends.rank(ascending=True)
    df['health_rank'] = df.health.rank(ascending=True)
    df['performance_rank'] = df.performance.rank(ascending=True)
    df['valuation_rank'] = df.valuation.rank(ascending=True)
    df['Score'] = df['dividends_rank'] + df['health_rank'] +  df['performance_rank'] + df[
        'valuation_rank']
    df = df.sort_values(by='Score', ascending=False)
    return df


def execute(watchlist_location):
    company_list = []
    for loc in watchlist_location:
        company_list += [line.rstrip('\n') for line in open(loc)]

    c_score_dict = {}
    s_score_dict = {}
    error_list = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # Start the load operations and mark each future with its URL

        future_score = {}

        for code in company_list:
            is_bse = False
            if code.isnumeric():
                is_bse = True
            l = DataAccess.get_company_code(code, is_bse)
            if l:
                comp = l[0]['symbol']
                future_score.update({executor.submit(Analyzer.analyse, comp): comp})

        for future in concurrent.futures.as_completed(future_score):
            company = future_score[future]
            try:
                scores_combined = future.result(timeout=10)
                print('-' * 100)
                print('Company - {}'.format(company))
                print(scores_combined)
                print('-' * 100)

                for key in ['standalone', 'consolidated']:
                    scores = scores_combined[key]
                    flat_dict = {
                        'valuation':scores['valuation']['score'],
                        'valuation_checklist':scores['valuation']['checks'],
                        'performance': scores['performance']['score'],
                        'performance_checklist': scores['performance']['checks'],
                        'health': scores['health']['score'],
                        'health_checklist': scores['health']['checks'],
                        'dividends': scores['dividends']['score'],
                        'dividends_checklist': scores['dividends']['checks']
                    }
                    if key is 'standalone':
                        s_score_dict.update({company: flat_dict})

                    if key is 'consolidated':
                        c_score_dict.update({company: flat_dict})
            except Exception as exc:
                print('%r generated an exception: %s' % (company, exc))
                error_list.append(company)

    df_c = pd.DataFrame(c_score_dict).transpose()
    df_s = pd.DataFrame(s_score_dict).transpose()

    df_c = assign_ranks(df_c).reset_index()
    df_s = assign_ranks(df_s).reset_index()

    df_s.rename(columns={'index': 'company'}).to_csv(resolve_data("report_standalone.csv"), index=False)
    df_c.rename(columns={'index': 'company'}).to_csv(resolve_data("report_consolidated.csv"), index=False)

    print('*' * 100)
    print("Following companies have errors. Analyse Manually: {}".format(error_list))

    with open(resolve_data("error_list.csv"), "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        for val in error_list:
            writer.writerow([val])

if __name__ == "__main__":
    execute(['/Users/Udit/Dropbox/Watchlist/watchlist_bse.tls',
             '/Users/Udit/Dropbox/Watchlist/watchlist.tls'])

