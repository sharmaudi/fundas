from celery_once import QueueOnce

from app.app import create_celery_app, create_app
from app.blueprints.api.models import CompanyInfo, Technicals, LatestStandalone, LatestConsolidated
from app.util import BhavcopyDownloader
from app.util.TaskHandler import TaskHandler

celeryApp = create_celery_app()
app = celeryApp.app
celery = celeryApp.celery

task_handler = TaskHandler(app=app)

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


@celery.task(base=QueueOnce, once={'graceful': True})
def update_companies():
    print("Update Companies Started.")

    with app.app_context():
        all_companies = CompanyInfo.query.all()
        task_handler.update_company_details(all_companies, workers=2, batch_size=200)


@celery.task(base=QueueOnce, once={'graceful': True})
def update_screener():
    print("Update screener Started.")
    with app.app_context():
        all_companies = CompanyInfo.query.all()
        task_handler.update_screener_details(all_companies, workers=2, batch_size=500)


