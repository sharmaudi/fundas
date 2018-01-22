import pickle

from app.util import Analyzer, DataAccess
from app.util.PathResolver import resolve_data


def execute(watchlist_location='/dropbox', app=None):
    featured = DataAccess.get_featured_companies(location=watchlist_location)
    df_c, error_list = Analyzer.analyse_list(featured, app=app)
    pickle.dump(df_c, open(resolve_data('featured.pkl'), "wb"))

if __name__ == "__main__":
    execute(watchlist_location='/Users/Udit/Dropbox/Watchlist')

