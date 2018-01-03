from app.util import Analyzer


def execute(watchlist_location):
    company_list = []
    for loc in watchlist_location:
        company_list += [line.rstrip('\n') for line in open(loc)]
    Analyzer.analyse_list(company_list, 'report')

if __name__ == "__main__":
    execute(['/Users/Udit/Dropbox/Watchlist/watchlist_bse.tls',
             '/Users/Udit/Dropbox/Watchlist/watchlist.tls'])

