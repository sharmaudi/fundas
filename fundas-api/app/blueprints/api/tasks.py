from app.app import create_celery_app, create_app
from app.util import BhavcopyDownloader

celeryApp = create_celery_app()
app = celeryApp.app
celery = celeryApp.celery


@celery.task(bind=True)
def analyse_watchlist_task(self):
    print("Analysing watchlist")
    from app.util import analyse_watchlist as aw
    aw.execute(app=app)
    return {
        'status': 'done',
        'progress': 100
    }


@celery.task(bind=True)
def analyse_portfolio_task(self):
    print("Analysing portfolio")
    from app.util import analyse_portfolio as ap
    ap.execute('/dropbox/tradebook.xlsx', app=app)
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
