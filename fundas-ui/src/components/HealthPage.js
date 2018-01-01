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
                    title={'Current Ratio'}
                    companyName={this.props.company}
                    dataSet={this.props.companyDataSet}
                    dataType={dataType}
                    period={'annual'}
                    chartType='line'
                    indicators={['CRATIO']}

                />

            </div>

            <div className="col-xs-12 col-sm-6 col-md-6 col-lg-6 col-md m-b-15">
                <Chart
                    title={'Solvency Ratio'}
                    companyName={this.props.company}
                    dataSet={this.props.companyDataSet}
                    dataType={dataType}
                    period={'annual'}
                    chartType='line'
                    indicators={['SOLRATIO']}

                />

            </div>

            <div className="col-xs-12 col-sm-6 col-md-6 col-lg-6 col-md m-b-15">
                <Chart
                    title={'Debt to Equity'}
                    companyName={this.props.company}
                    dataSet={this.props.companyDataSet}
                    dataType={dataType}
                    period={'annual'}
                    chartType='line'
                    indicators={['LTDE']}

                />

            </div>

            <div className="col-xs-12 col-sm-6 col-md-6 col-lg-6 col-md m-b-15">
                <Chart
                    title={'Interest Coverage'}
                    companyName={this.props.company}
                    dataSet={this.props.companyDataSet}
                    dataType={dataType}
                    period={'annual'}
                    chartType='line'
                    indicators={['IC']}

                />

            </div>

            <div className="col-xs-12 col-sm-6 col-md-6 col-lg-6 m-b-15">
                <Chart
                    title={'Debt to Assets Ratio'}
                    companyName={this.props.company}
                    dataSet={this.props.companyDataSet}
                    dataType={dataType}
                    period={'annual'}
                    chartType='line'
                    indicators={['DEBT_ASSETS']}
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
