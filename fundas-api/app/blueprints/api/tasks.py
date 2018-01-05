from app.app import create_celery_app
from app.util import BhavcopyDownloader

celery = create_celery_app()


@celery.task(bind=True)
def analyse_watchlist_task(self):
    print("Analysing watchlist")
    from app.util import analyse_watchlist as aw
    aw.execute(['/dropbox/watchlist_bse.tls',
                               '/dropbox/watchlist.tls'])

    return {
        'status': 'done',
        'progress': 100
    }


@celery.task(bind=True)
def analyse_portfolio_task(self):
    print("Analysing portfolio")
    from app.util import analyse_portfolio as ap
    ap.execute('/dropbox/tradebook.xlsx')
    return {
        'status': 'done',
        'progress': 100
    }


@celery.task(bind=True)
def download_bhavcopy_task(self, period):
    print("Downloading Bhavcopies")

    BhavcopyDownloader.get_bse_bhavcopy(periods=period, save_location='/dropbox/eoddata/bse')
    BhavcopyDownloader.get_nse_bhavcopy(periods=period, save_location='/dropbox/eoddata/nse')

    return {
        'status': 'done',
        'progress': 100
    }


@celery.task()
def refresh_prices():
    print("Refreshing prices")
    return {
        'status': 'done',
        'progress': 100
    }


@celery.task()
def refresh_screener_data():
    print("Refreshing Screener data")
    return {
        'status': 'done',
        'progress': 100
    }
