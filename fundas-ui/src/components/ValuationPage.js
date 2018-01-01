import React, {Component} from 'react';
import Chart from "./Chart";
import compose from "recompose/compose";
import {connect} from "react-redux";
import withWidth from "material-ui/utils/withWidth";

class ValuationPage extends Component {
    render() {
        let {dataType} = this.props.match.params;
        dataType = dataType?dataType:'standalone';

        return (



        <div className="row">
            <div className="col-xs-12 col-sm-6 col-md-6 col-lg-6 col-md m-b-15">
                <Chart
                    title={'Price to Earnings'}
                    companyName={this.props.company}
                    dataSet={this.props.companyDataSet}
                    dataType={dataType}
                    period={'annual'}
                    chartType='line'
                    indicators={['PE']}

                />

            </div>


            <div className="col-xs-12 col-sm-6 col-md-6 col-lg-6 col-md m-b-15">
                <Chart
                    title={'Price to Book Value'}
                    companyName={this.props.company}
                    dataSet={this.props.companyDataSet}
                    dataType={dataType}
                    period={'annual'}
                    chartType='line'
                    indicators={['PBV']}

                />

            </div>


            <div className="col-xs-12 col-sm-6 col-md-6 col-lg-6 col-md m-b-15">
                <Chart
                    title={'PEG Ratio'}
                    companyName={this.props.company}
                    dataSet={this.props.companyDataSet}
                    dataType={dataType}
                    period={'annual'}
                    chartType='line'
                    indicators={['PEG']}

                />

            </div>

            <div className="col-xs-12 col-sm-6 col-md-6 col-lg-6 col-md m-b-15">
                <Chart
                    title={'PEG Ratio'}
                    companyName={this.props.company}
                    dataSet={this.props.companyDataSet}
                    dataType={dataType}
                    period={'annual'}
                    chartType='line'
                    indicators={['PEG']}

                />

            </div>

            <div className="col-xs-12 col-sm-6 col-md-6 col-lg-6 col-md m-b-15">
                <Chart
                    title={'CROCI - WACC Spread'}
                    companyName={this.props.company}
                    dataSet={this.props.companyDataSet}
                    dataType={dataType}
                    period={'annual'}
                    chartType='line'
                    indicators={['CROCI', 'WACC']}

                />

            </div>

            <div className="col-xs-12 col-sm-6 col-md-6 col-lg-6 col-md m-b-15">
                <Chart
                    title={'Price to Sales'}
                    companyName={this.props.company}
                    dataSet={this.props.companyDataSet}
                    dataType={dataType}
                    period={'annual'}
                    chartType='line'
                    indicators={['PS']}

                />

            </div>

            <div className="col-xs-12 col-sm-6 col-md-6 col-lg-6 col-md m-b-15">
                <Chart
                    title={'Enterprise Value'}
                    companyName={this.props.company}
                    dataSet={this.props.companyDataSet}
                    dataType={dataType}
                    period={'annual'}
                    chartType='line'
                    indicators={['EV']}

                />

            </div>

            <div className="col-xs-12 col-sm-6 col-md-6 col-lg-6 col-md m-b-15">
                <Chart
                    title={'Enterprise value to EBITDA'}
                    companyName={this.props.company}
                    dataSet={this.props.companyDataSet}
                    dataType={dataType}
                    period={'annual'}
                    chartType='line'
                    indicators={['EVEBIDTA']}

                />

            </div>

            <div className="col-xs-12 col-sm-6 col-md-6 col-lg-6 col-md m-b-15">
                <Chart
                    title={'Enterprise value to Sales'}
                    companyName={this.props.company}
                    dataSet={this.props.companyDataSet}
                    dataType={dataType}
                    period={'annual'}
                    chartType='line'
                    indicators={['EVREV']}

                />

            </div>

        </div>



        );


    }
}

ValuationPage.propTypes = {};
ValuationPage.defaultProps = {};

const mapStateToProps = state => {
    return {
        company: state.fundas.company,
        companyDataSet: state.fundas.companyDataSet,
        companies: state.common.companies
    }
};

const mapDispatchToProps = dispatch => ({});


export default compose(withWidth(), connect(mapStateToProps, mapDispatchToProps))(ValuationPage);
