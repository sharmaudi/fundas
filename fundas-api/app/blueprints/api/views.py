from flask import Blueprint, jsonify, current_app, Response
import time

from flask_cors import cross_origin

from app.blueprints.api.models import CompanyInfo
from app.util import DataAccess, report, ConfigLoader, DBUtil
from flask import request

from app.util.Analyzer import analyse_company

api = Blueprint('api', __name__, template_folder='templates')

import simplejson as json


@api.route('/api/v1/companies', methods=['GET'])
@api.route('/api/v1/companies/', methods=['GET'])
@cross_origin()
def get_all_symbols():
    data = {'companies': DataAccess.get_all_symbols()}
    return jsonify(data)


@api.route('/api/v1/companies/<company>', methods=['GET'])
@api.route('/api/v1/companies/<company>', methods=['GET'])
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
        'technicals': data_df.to_dict(orient='records')
    }
    end_time = time.time()
    print('Processed Request at {}' + str(end_time))
    print('Time take to process request : {} seconds'.format(str(end_time - start_time)))
    return jsonify(data)


@api.route('/api/v1/portfolio', methods=['GET'])
@api.route('/api/v1/portfolio/', methods=['GET'])
def get_portfolio():
    return as_json(report.get_portfolio_report())


@api.route('/api/v1/featured', methods=['GET'])
@api.route('/api/v1/featured/', methods=['GET'])
@cross_origin()
def get_featured():
    return jsonify(report.get_report())


@api.route('/api/v1/portfolio/performance', methods=['GET'])
@api.route('/api/v1/portfolio/performance/', methods=['GET'])
@cross_origin()
def get_portfolio_performance():
    return as_json(report.get_portfolio_performance_report())


def as_json(data):
    return Response(response=json.dumps(data, ignore_nan=True),
                    mimetype='application/json')