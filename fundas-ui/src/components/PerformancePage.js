import React, {Component} from 'react';
import Chart from "./Chart";
import compose from "recompose/compose";
import {connect} from "react-redux";
import withWidth from "material-ui/utils/withWidth";


class ChartsPage extends Component {
    render() {
        let {dataType} = this.props.match.params;

        dataType = dataType?dataType:'standalone';

        return (

        <div className="row">
            <div className="col-xs-12 col-sm-6 col-md-6 col-lg-6 col-md m-b-15">
                <Chart
                    title={'Annual Performance'}
                    companyName={this.props.company}
                    dataSet={this.props.companyDataSet}
                    dataType={dataType}
                    period={'annual'}
                    chartType='area'
                    indicators={['SR', 'NP', 'OP']}

                />

            </div>

            <div className="col-xs-12 col-sm-6 col-md-6 col-lg-6 m-b-15">
                <Chart
                    title={'Quarterly Performance'}
                    companyName={this.props.company}
                    dataSet={this.props.companyDataSet}
                    dataType={dataType}
                    period={'quarterly'}
                    chartType='area'
                    indicators={['SR', 'NP', 'OP']}

                />
            </div>

            <div className="col-xs-12 col-sm-6 col-md-6 col-lg-6 m-b-15">
                <Chart
                    title={'Annual Margins'}
                    companyName={this.props.company}
                    dataSet={this.props.companyDataSet}
                    dataType={dataType}
                    period={'annual'}
                    chartType='area'
                    indicators={['OPMPCT', 'NETPCT', 'EBIDTPCT']}
                />
            </div>

            <div className="col-xs-12 col-sm-6 col-md-6 col-lg-6 m-b-15">
                <Chart
                    title={'Quarterly Margins'}
                    companyName={this.props.company}
                    dataSet={this.props.companyDataSet}
                    dataType={dataType}
                    period={'quarterly'}
                    chartType='area'
                    indicators={['OPMPCT', 'NETPCT', 'EBIDTPCT']}
                />
            </div>

            <div className="col-xs-12 col-sm-6 col-md-6 col-lg-6 m-b-15">
                <Chart
                    title={'Net Margin'}
                    companyName={this.props.company}
                    dataSet={this.props.companyDataSet}
                    dataType={dataType}
                    period={'annual'}
                    chartType='line'
                    indicators={['NETPCT']}
                />
            </div>

            <div className="col-xs-12 col-sm-6 col-md-6 col-lg-6 m-b-15">
                <Chart
                    title={'Net Income and Cash from Operations'}
                    companyName={this.props.company}
                    dataSet={this.props.companyDataSet}
                    dataType={dataType}
                    period={'annual'}
                    chartType='line'
                    indicators={['NP', 'CFO']}
                />
            </div>

            <div className="col-xs-12 col-sm-6 col-md-6 col-lg-6 m-b-15">
                <Chart
                    title={'ROE - ROCE'}
                    companyName={this.props.company}
                    dataSet={this.props.companyDataSet}
                    dataType={dataType}
                    period={'annual'}
                    chartType='line'
                    indicators={['ROE', 'ROCE']}
                />
            </div>

            <div className="col-xs-12 col-sm-6 col-md-6 col-lg-6 m-b-15">
                <Chart
                    title={'Earnings per share'}
                    companyName={this.props.company}
                    dataSet={this.props.companyDataSet}
                    dataType={dataType}
                    period={'annual'}
                    chartType='bar'
                    indicators={['EPS']}
                />
            </div>

            <div className="col-xs-12 col-sm-6 col-md-6 col-lg-6 m-b-15">
                <Chart
                    title={'Return on Assets'}
                    companyName={this.props.company}
                    dataSet={this.props.companyDataSet}
                    dataType={dataType}
                    period={'annual'}
                    chartType='line'
                    indicators={['ROA']}
                />
            </div>

            <div className="col-xs-12 col-sm-6 col-md-6 col-lg-6 m-b-15">
                <Chart
                    title={'CROCI'}
                    companyName={this.props.company}
                    dataSet={this.props.companyDataSet}
                    dataType={dataType}
                    period={'annual'}
                    chartType='line'
                    indicators={['CROCI']}
                />
            </div>

        </div>

        );


    }
}

ChartsPage.propTypes = {};
ChartsPage.defaultProps = {};

const mapStateToProps = state => {
    return {
        company: state.fundas.company,
        companyDataSet: state.fundas.companyDataSet,
        companies: state.common.companies
    }
};

const mapDispatchToProps = dispatch => ({});


export default compose(withWidth(), connect(mapStateToProps, mapDispatchToProps))(ChartsPage);
