import React, {Component} from 'react';
import PropTypes from 'prop-types';
import compose from "recompose/compose";
import withWidth from "material-ui/utils/withWidth";
import ReactHighchart from 'react-highcharts'

class EquityCurveChart extends Component {



    getConfig() {
        const perf = this.props.portfolio.performance;
        return {
            chart: {
                type: 'line'
            },
            title: {
                text: 'Equity Curve'
            },
            subtitle: {
                text: 'Portfolio performance against indices'
            },
            xAxis: {
                type: 'datetime',

                title: {
                    text: 'Date'
                }
            },
            yAxis: {
                title: {
                    text: 'Equity'
                },
                min: perf.equityCurveMinValue,
                max: perf.equityCurveMaxValue
            },
            tooltip: {
                headerFormat: '<b>{series.name}</b><br>',
                pointFormat: '{point.x:%e. %b}: {point.y:.2f} %'
            },

            plotOptions: {
                spline: {
                    marker: {
                        enabled: true
                    }
                }
            },

            series: [{
                name: 'Portfolio',
                data: perf.equityCurve
            }, {
                name: 'JUNIORBEES',
                data: perf.equityCurveJNF
            }, {
                name: 'NIFTYBEES',
                data: perf.equityCurveNF
            }]
        }


    }


    render() {
        return (
            <div>
                <ReactHighchart config={this.getConfig()}/>
            </div>
        );
    }
}

EquityCurveChart.propTypes = {
    title:PropTypes.string,
    portfolio:PropTypes.object,
};

EquityCurveChart.defaultProps = {
    title:"Equity Curve"
};

export default compose(withWidth())(EquityCurveChart);
