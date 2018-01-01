import React, {Component} from 'react';
import Chart from "./Chart";
import compose from "recompose/compose";
import {connect} from "react-redux";
import withWidth from "material-ui/utils/withWidth";

class DividendsPage extends Component {
    render() {

        let {dataType} = this.props.match.params;
        dataType = dataType||'standalone';

        return (



        <div className="row">
            <div className="col-xs-12 col-sm-6 col-md-6 col-lg-6 col-md m-b-15">
                <Chart
                    title={'Dividends'}
                    companyName={this.props.company}
                    dataSet={this.props.companyDataSet}
                    dataType={dataType}
                    period={'annual'}
                    chartType='bar'
                    indicators={['DIV']}

                />

            </div>


            <div className="col-xs-12 col-sm-6 col-md-6 col-lg-6 col-md m-b-15">
                <Chart
                    title={'Dividend Payout'}
                    companyName={this.props.company}
                    dataSet={this.props.companyDataSet}
                    dataType={dataType}
                    period={'annual'}
                    chartType='line'
                    indicators={['DIVPAY']}

                />

            </div>

            <div className="col-xs-12 col-sm-6 col-md-6 col-lg-6 col-md m-b-15">
                <Chart
                    title={'Dividend Yield'}
                    companyName={this.props.company}
                    dataSet={this.props.companyDataSet}
                    dataType={dataType}
                    period={'annual'}
                    chartType='line'
                    indicators={['DIVYLD']}

                />

            </div>


        </div>


        );


    }
}

DividendsPage.propTypes = {};
DividendsPage.defaultProps = {};

const mapStateToProps = state => {
    return {
        company: state.fundas.company,
        companyDataSet: state.fundas.companyDataSet,
        companies: state.common.companies
    }
};

const mapDispatchToProps = dispatch => ({});


export default compose(withWidth(), connect(mapStateToProps, mapDispatchToProps))(DividendsPage);
