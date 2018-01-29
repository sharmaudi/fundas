import concurrent.futures
import concurrent.futures
import datetime

from app.blueprints.api.models import Technicals, LatestStandalone, LatestConsolidated, \
    TechnicalsHistorical
from app.util import DataAccess, ScreenerUtil


class TaskHandler:
    app = None

    def __init__(self, app=None):
        if not app:
            from flask import current_app
            self.app = current_app
        else:
            self.app = app

    def get_technicals(self, info):
        with self.app.app_context():
            # print(f"[{info.symbol} - Getting technicals]")
            l_s = Technicals.query.get(info.symbol)

            if l_s:
                diff = (datetime.datetime.now() - l_s.updated_on).total_seconds() / (60.0 * 60.0)
                if diff < 24:
                    raise ValueError(f"[{info.symbol}] Technicals updated just {diff} hours ago.")
            return DataAccess.get_technicals(info.symbol, info=info)


    def get_screener_details(self, info):
        with self.app.app_context():
            l_s = LatestStandalone.query.get(info.symbol)

            if l_s:
                diff = (datetime.datetime.now() - l_s.updated_on).total_seconds() / (60.0 * 60.0)
                if diff < 24:
                    raise ValueError(f"[{info.symbol}] Screener details updated just {diff} hours ago.")
            return ScreenerUtil.get_screener_dicts(company_info=info)

    def process_in_batch(self, company_list, executor_function, bulk_update_function, workers=2, batch_size=50, ):
        current_batch = 1
        for i in range(0, len(company_list), batch_size):
            print(f"Processing Batch {current_batch}")
            batch = company_list[i:i + batch_size]
            res_list = []
            with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
                future_result = {}
                for info in batch:
                    future_result.update({executor.submit(executor_function, info): info.symbol})

                for future in concurrent.futures.as_completed(future_result):
                    c = future_result[future]
                    try:
                        r = future.result(timeout=500)
                        if r:
                            res_list.append(r)
                    except Exception as ex:
                        print(f"[{c}] threw Exception: {ex}")

            if res_list:
                print(f"Updating database for {len(res_list)} records")
                bulk_update_function(res_list)
            current_batch += 1

    def update_company_details(self, company_list, workers=2, batch_size=30):
        self.process_in_batch(company_list,
                              self.get_technicals,
                              self.bulk_update,
                              workers=workers,
                              batch_size=batch_size)

    def update_screener_details(self, company_list, workers=2, batch_size=30):
        self.process_in_batch(company_list,
                              self.get_screener_details,
                              self.bulk_update_screener,
                              workers=workers,
                              batch_size=batch_size)

    def bulk_update_screener(self, res_list):
        objects1 = []
        objects2 = []
        from app.extensions import db
        if res_list:
            for c in res_list:
                try:
                    latest_std, latest_con = self.get_screener_models(c)
                    objects1.append(latest_std)
                    objects2.append(latest_con)
                except Exception as ex:
                    print(f"Exception while generating models from resultset: {c}: {ex}")
            print(f"Saving {len(objects1)} standalone records to database")
            print(f"Saving {len(objects2)} consolidated records to database")
            db.session.bulk_save_objects(objects1)
            db.session.bulk_save_objects(objects2)
            db.session.commit()

    def bulk_update(self, res_list):
        from app.extensions import db
        objects = []
        if res_list:
            for c in res_list:

                try:
                    comp = c['company']
                    print(f'[{comp}] - deleting')
                    Technicals.query.filter(Technicals.symbol == c['company']).delete()
                    db.session.commit()
                    technicals = self.get_models(c)
                    objects.append(technicals)

                    for hist in technicals.historicals:
                        objects.append(hist)

                except Exception as ex:
                    print(f"[{c['company']}Exception while generating models from resultset: {c['company']}: {ex}")

            print(f"Saving {len(objects)} records to database")
            db.session.bulk_save_objects(objects)
            db.session.commit()

    def get_models(self, c):
        technicals = Technicals()
        df = c['technicals']
        technicals.symbol = c['company']
        technicals.latest_price = df.iloc[-1].Close
        technicals.splits = {},
        technicals.roc30 = df.iloc[-1].roc_30
        technicals.roc60 = df.iloc[-1].roc_60
        technicals.hhv52 = df.iloc[-1].hhv_52
        technicals.hhv_all_time = df.iloc[-1].hhv_all_time

        for index, row in df.iterrows():
            hist = TechnicalsHistorical()
            hist.symbol = technicals.symbol
            hist.date = index.strftime('%Y-%m-%d')
            hist.open = row['Open']
            hist.high = row['High']
            hist.low = row['Low']
            hist.close = row['Close']
            hist.volume = row['Volume']
            hist.roc30 = row['roc_30']
            hist.roc60 = row['roc_60']
            hist.hhv52 = row['hhv_52']
            hist.hhv_all_time = row['hhv_all_time']
            technicals.historicals.append(hist)

        return technicals

    def get_screener_models(self, d):

        symbol = d['info'].symbol

        l_s = LatestStandalone.query.get(symbol)
        l_c = LatestConsolidated.query.get(symbol)

        if not l_s:
            l_s = LatestStandalone()
            l_s.symbol = symbol

        if not l_c:
            l_c = LatestConsolidated()
            l_c.symbol = symbol

        if 'book_value' in d['standalone']:
            l_s.book_value = d['standalone']['book_value']
        if 'current_price' in d['standalone']:
            l_s.current_price = d['standalone']['current_price']
        if 'face_value' in d['standalone']:
            l_s.face_value = d['standalone']['face_value']
        if 'market_capitalization' in d['standalone']:
            l_s.market_cap = d['standalone']['market_capitalization']
        if 'price_to_earning' in d['standalone']:
            l_s.price_to_earning = d['standalone']['price_to_earning']
        if 'analysis' in d['standalone']:
            l_s.analysis = d['standalone']['analysis']

        if 'book_value' in d['consolidated']:
            l_c.book_value = d['consolidated']['book_value']
        if 'current_price' in d['consolidated']:
            l_c.current_price = d['consolidated']['current_price']
        if 'face_value' in d['consolidated']:
            l_c.face_value = d['consolidated']['face_value']
        if 'market_capitalization' in d['consolidated']:
            l_c.market_cap = d['consolidated']['market_capitalization']
        if 'price_to_earning' in d['consolidated']:
            l_c.price_to_earning = d['consolidated']['price_to_earning']
        if 'analysis' in d['consolidated']:
            l_c.analysis = d['consolidated']['analysis']

        return l_s, l_c
