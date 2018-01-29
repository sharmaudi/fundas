import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from app.extensions import db
from app.mixins.sqlalchemy_resource_mixin import ResourceMixin
from app.util import ScreenerUtil
import time


class CompanyInfo(db.Model, ResourceMixin):
    __tablename__ = 'company_info'
    symbol = db.Column(db.String, primary_key=True)
    isin_code = db.Column(db.String)
    bse_code = db.Column(db.String(256))
    bse_id = db.Column(db.String(256))
    nse_code = db.Column(db.String(128))
    bse_name = db.Column(db.String())
    nse_name = db.Column(db.String())
    sector = db.Column(db.String())
    industry = db.Column(db.String())
    quandl_code = db.Column(db.String())
    screener_code = db.Column(db.String(128))

    @classmethod
    def find_by_symbol(cls, symbol):
        current_datetime = datetime.datetime.utcnow()
        info = CompanyInfo.query.get(symbol)
        l_s = LatestStandalone.query.get(symbol)
        l_c = LatestConsolidated.query.get(symbol)

        if not l_s or not l_c:
            print('Company doesnt exist in database. Getting details from Screener')
            info, l_s, l_c = CompanyInfo.create_from_screener(info)
        return info, l_s, l_c

    @classmethod
    def create_from_screener(cls, info):

        l_s = LatestStandalone.query.get(info.symbol)
        l_c = LatestConsolidated.query.get(info.symbol)

        if not l_s:
            l_s = LatestStandalone()

        if not l_c:
            l_c = LatestConsolidated()

        d = None
        try:
            d = ScreenerUtil.get_screener_dicts(company_info=info)

            l_s.symbol = info.symbol
            l_s.book_value = d['standalone']['book_value']
            l_s.current_price = d['standalone']['current_price']
            l_s.face_value = d['standalone']['face_value']
            l_s.market_cap = d['standalone']['market_capitalization']
            l_s.price_to_earning = d['standalone']['price_to_earning']
            l_s.analysis = d['standalone']['analysis']
            l_s.save()

            l_c.symbol = info.symbol
            l_c.book_value = d['consolidated']['book_value']
            l_c.current_price = d['consolidated']['current_price']
            l_c.face_value = d['consolidated']['face_value']
            l_c.market_cap = d['consolidated']['market_capitalization']
            l_c.price_to_earning = d['consolidated']['price_to_earning']
            l_c.analysis = d['consolidated']['analysis']
            l_c.save()

        except Exception as e:
            f"Exception while getting details from screener for {info.symbol}. Exeption: {e}"

        info.updated_on = datetime.datetime.utcnow()
        info.save()
        db.session.commit()
        return info, l_s, l_c


class LatestStandalone(db.Model, ResourceMixin):
    __tablename__ = 'latest_standalone'
    symbol = db.Column(db.String, primary_key=True)
    book_value = db.Column(db.Float)
    current_price = db.Column(db.Float)
    face_value = db.Column(db.Float)
    market_cap = db.Column(db.Float)
    price_to_earning = db.Column(db.Float)
    roc_30 = db.Column(db.Float)
    analysis = db.Column(db.JSON)


class LatestConsolidated(db.Model, ResourceMixin):

    __tablename__ = 'latest_consolidated'
    symbol = db.Column(db.String, primary_key=True)
    book_value = db.Column(db.Float)
    current_price = db.Column(db.Float)
    face_value = db.Column(db.Float)
    market_cap = db.Column(db.Float)
    price_to_earning = db.Column(db.Float)
    roc_30 = db.Column(db.Float)
    analysis = db.Column(db.JSON)


class Technicals(db.Model, ResourceMixin):
    __tablename__ = 'technicals'
    symbol = db.Column(db.String, primary_key=True)
    historicals = relationship('TechnicalsHistorical',
                               cascade="all, delete-orphan")
    latest_price = db.Column(db.Float)
    splits = db.Column(db.JSON)
    roc30 = db.Column(db.Float)
    roc60 = db.Column(db.Float)
    hhv52 = db.Column(db.Float)
    hhv_all_time = db.Column(db.Float)


class TechnicalsHistorical(db.Model, ResourceMixin):
    __tablename__ = 'techinals_historical'
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String, ForeignKey('technicals.symbol', ondelete='CASCADE'))
    date = db.Column(db.Date)
    open = db.Column(db.Float)
    high = db.Column(db.Float)
    low = db.Column(db.Float)
    close = db.Column(db.Float)
    volume = db.Column(db.Float)
    hhv52 = db.Column(db.Float)
    hhv_all_time = db.Column(db.Float)
    roc30 = db.Column(db.Float)
    roc60 = db.Column(db.Float)


class Watchlist(db.Model, ResourceMixin):
    __tablename__ = 'watchlist'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String)
    symbol = db.Column(db.String)
