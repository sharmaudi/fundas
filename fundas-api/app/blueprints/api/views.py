import pickle

import datetime
from flask import Blueprint, jsonify, current_app, Response
import time

from flask_cors import cross_origin

from app.blueprints.api.models import CompanyInfo, Watchlist
from app.extensions import csrf, db
from app.util import DataAccess, report, ConfigLoader, DBUtil, Analyzer
from flask import request

from app.util.Analyzer import analyse_company
from app.util.PathResolver import resolve_data

api = Blueprint('api', __name__, template_folder='templates')

import simplejson as json


@api.route('/api/v1/companies', methods=['GET'])
@api.route('/api/v1/companies/', methods=['GET'])
@cross_origin()
def get_all_symbols():
    data = {'companies': [rec.symbol for rec in CompanyInfo.query.all()]}
    return jsonify(data)


@api.route('/api/v1/companies/<company>', methods=['GET'])
@api.route('/api/v1/companies/<company>/', methods=['GET'])
@cross_origin()
def company_details(company):
    start_time = time.time()
    print('Received Request at {}'.format(str(start_time)))

    info, latest_s, latest_c = CompanyInfo.find_by_symbol(company)
    df = DataAccess.get_company_dataframe(company,
                                          info=info,
                                          latest_standalone=latest_s,
                                          latest_consolidated=latest_c)
    data = DataAccess.get_data(company, company_dfs=df)
    s_data = None
    c_data = None
    try:
        s_data = analyse_company(company, company_dataframe=df, data_type='standalone')
    except Exception as e:
        print(f"Error while analysing ${company} in standalone. Exception: ${e}")

    try:
        c_data = analyse_company(company, company_dataframe=df, data_type='consolidated')
    except Exception as e:
        print(f"Error while analysing ${company} in consolidated. Exception: ${e}")

    if s_data or c_data:
        data['analysis'] = {
            'standalone': s_data,
            'consolidated': c_data
        }

        data['company_info'] = DBUtil.to_json(info)

        data['latest_standalone'] = DBUtil.to_json(latest_s)
        data['latest_consolidated'] = DBUtil.to_json(latest_c)

    end_time = time.time()
    print('Processed Request at {}'.format(str(end_time)))

    print('Time take to process request : {} seconds'.format(str(end_time - start_time)))

    return as_json(data)


@api.route('/api/v1/companies/<company>/analysis', methods=['GET'])
@api.route('/api/v1/companies/<company>/analysis/', methods=['GET'])
def analyse(company):
    company_dfs = DataAccess.get_company_dataframe(company)
    s_data = {}
    c_data = {}

    try:
        s_data = analyse_company(company, company_dataframe=company_dfs, data_type='standalone')
    except Exception as e:
        print(f"Error while analysing ${company} in standalone. Exception: ${e}")


    try:
        c_data = analyse_company(company, company_dataframe=company_dfs, data_type='consolidated')
    except Exception as e:
        print(f"Error while analysing ${company} in consolidated. Exception: ${e}")

    data = {
        'standalone': s_data,
        'consolidated': c_data
    }

    return as_json(data)


@api.route('/api/v1/companies/<company>/momentum', methods=['GET'])
@api.route('/api/v1/companies/<company>/momentum/', methods=['GET'])
@cross_origin()
def get_momentum(company):
    start_time = time.time()
    print('Received Request at {}'.format(str(start_time)))
    data_df = DBUtil.get_technicals_as_df(company)
    data = {
        'company': company,
        'technicals': data_df.reset_index().to_dict(orient='records')
    }
    end_time = time.time()
    print('Processed Request at {}' + str(end_time))
    print('Time take to process request : {} seconds'.format(str(end_time - start_time)))
    return jsonify(data)


@api.route('/api/v1/portfolio', methods=['GET'])
@api.route('/api/v1/portfolio/', methods=['GET'])
@cross_origin()
def get_portfolio():


    companies = None

    try:
        companies = pickle.load(open(resolve_data('portfolio-companies.pkl'), "rb"))
    except Exception as ex:
        print(f"Error while reading portfolio companies: {ex}")

    ret_dict = {
        'companies': companies,
        'performance': report.get_portfolio_performance_report()
    }

    return as_json(ret_dict)


@api.route('/api/v1/featured', methods=['GET'])
@api.route('/api/v1/featured/', methods=['GET'])
@cross_origin()
def get_featured():
    featured = pickle.load(open(resolve_data('featured.pkl'), "rb"))
    return as_json(featured)


def get_company_snapshot(comp):

    info = CompanyInfo.query.get(comp)

    df = DataAccess.get_company_dataframe(comp,
                                          info=info)
    data = DataAccess.get_data(comp, company_dfs=df, indicators=['SR'])
    return {
        'info': DBUtil.to_json(info),
        'data': data
    }

def get_featured_companies():
    company_list = []
    featured = ['/dropbox/watchlist_bse.tls',
                               '/dropbox/watchlist.tls']
    for list in featured:
        company_list += [line.rstrip('\n') for line in open(list)]
    return company_list

@api.route('/api/v1/portfolio/performance', methods=['GET'])
@api.route('/api/v1/portfolio/performance/', methods=['GET'])
@cross_origin()
def get_portfolio_performance():
    return jsonify(report.get_portfolio_performance_report())


@api.route('/api/v1/tasks/<task_name>/status/<task_id>', methods=['GET'])
@api.route('/api/v1/tasks/<task_name>/status/<task_id>/', methods=['GET'])
@cross_origin()
def taskstatus(task_name, task_id):
    print(f"Task Name: {task_name}")
    task_impl = None
    if task_name == 'analyse_watchlist':
        from app.blueprints.api.tasks import analyse_watchlist_task
        task_impl = analyse_watchlist_task
    elif task_name == 'analyse_portfolio':
        from app.blueprints.api.tasks import analyse_portfolio_task
        task_impl = analyse_portfolio_task
    elif task_name == 'download_bhavcopy':
        from app.blueprints.api.tasks import download_bhavcopy_task
        task_impl = download_bhavcopy_task

    if task_impl:
        task = task_impl.AsyncResult(task_id)
        if task.state == 'PENDING':
            # job did not start yet
            response = {
                'state': task.state,
                'current': 0,
                'total': 1,
                'status': 'Pending...'
            }
        elif task.state != 'FAILURE':
            response = {
                'state': task.state,
                'current': task.info.get('current', 0),
                'total': task.info.get('total', 1),
                'status': task.info.get('status', '')
            }
            if 'result' in task.info:
                response['result'] = task.info['result']
        else:
            # something went wrong in the background job
            response = {
                'state': task.state,
                'current': 1,
                'total': 1,
                'status': str(task.info),  # this is the exception raised
            }
    else:
        response = {
            'state': 'Task not found',
            'status': 'error'
        }
    return jsonify(response)


@api.route('/api/v1/watchlist', methods=['POST', 'PUT'])
@api.route('/api/v1/watchlist/', methods=['POST', 'PUT'])
@csrf.exempt
@cross_origin()
def add_to_watchlist():
    symbol = request.get_json(force=True)['symbol']

    is_valid = CompanyInfo.query.get(symbol)

    if not is_valid:
        return jsonify({
            "status": "failed",
            "message": "Symbol doesn't exist"
        }), 400

    existing = None
    try:
        existing = Watchlist.query.filter(Watchlist.symbol == symbol).first()
    except Exception as ex:
        print("Table watchlist doesnt exist. Creating..")
        Watchlist.__table__.create(db.session.bind)
        db.session.commit()

    if existing:
        return jsonify({
            "status": "failed",
            "message": "Already present in watchlist"
        }), 400
    else:
        watchlist = Watchlist()
        watchlist.symbol = symbol
        watchlist.user_id = 'bambebo'
        watchlist.save()
        return jsonify(get_watchlist_from_db()), 201


# @api.route('/api/v1/watchlist/<symbol>', methods=['DELETE'])
@api.route('/api/v1/watchlist/<symbol>/', methods=['DELETE'])
@csrf.exempt
@cross_origin()
def remove_from_watchlist(symbol):

    existing = None
    try:
        existing = Watchlist.query.filter(Watchlist.symbol == symbol).first()
    except Exception as ex:
        print("Table watchlist doesnt exist. Creating..")
        Watchlist.__table__.create(db.session.bind)
        db.session.commit()

    if not existing:
        return jsonify({
            "status": "failed",
            "message": "Symbol not found in watchlist"
        }), 400
    else:
        db.session.delete(existing)
        db.session.commit()
        return jsonify(get_watchlist_from_db()), 200


@api.route('/api/v1/watchlist', methods=['GET'])
@api.route('/api/v1/watchlist/', methods=['GET'])
@csrf.exempt
@cross_origin()
def get_watchlist():
    watchlist = get_watchlist_from_db()
    analyse_param = str(request.args.get('analyse'))
    analysis = None
    if analyse_param == 'true' or analyse_param == 'True':
        analysis = [Analyzer.analyse(item) for item in items]
    watchlist['analysis'] = analysis
    return jsonify(watchlist), 200


def get_watchlist_from_db():
    items = []
    try:
        watchlist = Watchlist.query.all()
        items = [item.symbol for item in watchlist]
    except Exception as ex:
        print("Table watchlist doesnt exist. Creating..")
        Watchlist.__table__.create(db.session.bind)
        db.session.commit()
    return {
        'watchlist': items
    }

@api.route('/api/v1/tasks/analyse_watchlist', methods=['GET'])
@api.route('/api/v1/tasks/analyse_watchlist/', methods=['GET'])
@cross_origin()
def analyse_watchlist():
    from app.blueprints.api.tasks import analyse_watchlist_task
    task = analyse_watchlist_task.delay()

    return jsonify({
        'task_id': task.id
    }), 202


@api.route('/api/v1/tasks/analyse_portfolio', methods=['GET'])
@api.route('/api/v1/tasks/analyse_portfolio/', methods=['GET'])
@cross_origin()
def analyse_portfolio():
    from app.blueprints.api.tasks import analyse_portfolio_task
    task = analyse_portfolio_task.delay()

    return jsonify({
        'task_id': task.id
    }), 202


@api.route('/api/v1/tasks/download_bhavcopy', methods=['POST'])
@api.route('/api/v1/tasks/download_bhavcopy/', methods=['POST'])
@csrf.exempt
@cross_origin()
def update_prices():
    periods = request.get_json(force=True)['periods']
    from app.blueprints.api.tasks import download_bhavcopy_task
    task = download_bhavcopy_task.delay(int(periods))

    return jsonify({
        'task_id': task.id
    }), 202


@api.route('/api/v1/tasks/update_companies', methods=['GET'])
@api.route('/api/v1/tasks/update_companies/', methods=['GET'])
@csrf.exempt
@cross_origin()
def update_companies():
    from app.blueprints.api.tasks import update_companies
    update_companies.delay()

    return jsonify({
        'status': 'success'
    }), 202


@api.route('/api/v1/tasks/update_screener', methods=['GET'])
@api.route('/api/v1/tasks/update_screener/', methods=['GET'])
@csrf.exempt
@cross_origin()
def update_screener():
    from app.blueprints.api.tasks import update_screener
    update_screener.delay()

    return jsonify({
        'status': 'success'
    }), 202



def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()


def as_json(data):
    return Response(response=json.dumps(data, ignore_nan=True, default=datetime_handler),
                    mimetype='application/json')
