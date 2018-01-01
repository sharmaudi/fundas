from flask import Blueprint, render_template
from app.util import ConfigLoader, report
import sys


fundas = Blueprint('fundas', __name__, template_folder='templates')

canEditWatchlists = False

if len(sys.argv) > 1 and sys.argv[1] == 'noupdate':
    canEditWatchlists = False


@fundas.route('/')
def home():
    return render_template('index.html')

@fundas.route('/fundas/')
@fundas.route('/fundas')
@fundas.route('/fundas/<string:category>', methods=['GET', 'POST'])
@fundas.route('/fundas/<string:category>/', methods=['GET', 'POST'])
def show_fundas(category=None):
    if not category:
        category = 'fundas'

    config = ConfigLoader.get_config_for(category)
    print(config)
    return render_template('fundas.html', config=config)


@fundas.route('/analysis')
@fundas.route('/analysis/')
def analysis():
    config = [
        {
            'id': 'valuation_check1',
            'rule': 'PE Ratio < NIFTY PE'
        },
        {
            'id': 'valuation_check2',
            'rule': 'PE Ratio < Industry PE'
        },
        {
            'id': 'valuation_check3',
            'rule': 'PE Ratio < 5 Year Average PE'
        },
        {
            'id': 'valuation_check4',
            'rule': 'PE Ratio < All time Average PE'
        },
        {
            'id': 'valuation_check5',
            'rule': 'PEG Ratio is within 0 and 1'
        },
        {
            'id': 'valuation_check6',
            'rule': 'EV/EBITDA < Industry average'
        },
        {
            'id': 'valuation_check7',
            'rule': 'PB Ratio < Industry PB Ratio'
        }
    ]

    performance_config = [
        {
            'id': 'performance_check1',
            'rule': '5 year EPS growth > Industry Average'
        },
        {
            'id': 'performance_check2',
            'rule': 'Todays EPS > EPS 5 years ago'
        },
        {
            'id': 'performance_check3',
            'rule': 'Current Year ROE > 20%'
        },
        {
            'id': 'performance_check4',
            'rule': 'Current Year ROCE > ROCE 3 years ago'
        },
        {
            'id': 'performance_check5',
            'rule': 'Current Year ROA > Industry Average'
        },
        {
            'id': 'performance_check6',
            'rule': 'Current Year CROCI > Industry Average'
        },
        {
            'id': 'performance_check7',
            'rule': 'Current Year Net Profit Margin > Industry Average'
        },

        {
            'id': 'performance_check9',
            'rule': 'Positive Quarterly profit growth'
        },
        {
            'id': 'performance_check10',
            'rule': 'Constantly growing top and bottom lines.'
        }
    ]

    health_config = [
        {
            'id': 'health_check1',
            'rule': 'Current Ratio > 1'
        },
        {
            'id': 'health_check2',
            'rule': 'Solvency Ratio > .2'
        },
        {
            'id': 'health_check3',
            'rule': 'Solvency Ratio > Solvency Ratio 3 Years ago'
        },
        {
            'id': 'health_check4',
            'rule': 'Debt to Equity <= Debt to Equity 5 years ago'
        },
        {
            'id': 'health_check5',
            'rule': 'Debt to Equity < 1'
        },
        {
            'id': 'health_check6',
            'rule': 'Interest Coverage ratio > 5'
        },
        {
            'id': 'health_check7',
            'rule': 'Debt to Asset ratio < .7'
        },
        {
            'id': 'health_check8',
            'rule': "Cash from Operations within 20% of Net profit for 3 consecutive years"
        }

    ]

    dividend_config = [
        {
            'id': 'dividends_check1',
            'rule': 'Dividend Yield > 3%'
        },
        {
            'id': 'dividends_check2',
            'rule': 'Dividend Yield > Industry Average'
        },
        {
            'id': 'dividends_check3',
            'rule': 'Latest total dividends have not fallen more than 25%'
        },
        {
            'id': 'dividends_check4',
            'rule': 'Total Dividends > Total Dividends 5 years ago'
        },
        {
            'id': 'dividends_check5',
            'rule': 'Dividend Payout > 0 and < 90'
        }

    ]

    momentum_config = [
        {
            'id': 'momentum_check1',
            'rule': '20 week ROC > 30'
        },
        {
            'id': 'momentum_check2',
            'rule': 'Price within 20% of 52 week high'
        }

    ]

    return render_template('/valuation.html'
                           , pe_config=config
                           , performance_config=performance_config
                           , health_config=health_config
                           , dividends_config=dividend_config
                           , momentum_config=momentum_config,
                           canEditWatchlists=canEditWatchlists
                           )


@fundas.route('/momentum')
@fundas.route('/momentum/')
def momentum():
    return render_template('momentum.html')


@fundas.route('/annual')
@fundas.route('/annual/')
def annual_reports():
    config = ConfigLoader.get_config_for("annual_reports")
    return render_template('reports.html', config=config)


@fundas.route('/quarterly')
@fundas.route('/quarterly/')
def quarterly_reports():
    config = ConfigLoader.get_config_for('quarterly_reports')
    return render_template('reports.html', config=config)


@fundas.route('/ratios')
@fundas.route('/ratios/')
def ratios():
    config = ConfigLoader.get_config_for('ratios')
    return render_template('reports.html', config=config)


@fundas.route('/watchlist')
@fundas.route('/watchlist/')
def watchlist():
    return render_template('watchlist.html', watchlist=report.get_report(), canEditWatchlists=False)


@fundas.route('/portfolio')
@fundas.route('/portfolio/')
def portfolio():
    return render_template('portfolio.html', portfolio=report.get_portfolio_report(), canEditWatchlists=False)

@fundas.route('/portfolio/performance')
@fundas.route('/portfolio/performance/')
def portfolio_performance():
    return render_template('portfolio-performance.html', portfolio=report.get_portfolio_performance_report(), canEditWatchlists=False)
