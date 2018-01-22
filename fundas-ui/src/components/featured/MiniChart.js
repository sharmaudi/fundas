import React, {Component} from 'react';
import PropTypes from 'prop-types';
import {blue50, red100, white} from 'material-ui/styles/colors';
import moment from 'moment'

import ReactHighchart from 'react-highcharts'
import compose from "recompose/compose";
import withWidth from 'material-ui/utils/withWidth';

const styles = {
    paper: {
        backgroundColor: white,
        height: 200
    },
    div: {
        marginLeft: 'auto',
        marginRight: 'auto',
        height: 150
    },
    header: {
        color: white,
        backgroundColor: blue50,
        padding: 10
    }
};

class MiniChart extends Component {

    createData() {
        const {indicators, dataSet, dataType, period} = this.props;

        if (dataSet) {
            //console.log(dataSet)
        }


        const myDataSet = dataSet[`${period}_${dataType}`];
        let returnData = [];

        if (myDataSet) {
            console.log(myDataSet);

            returnData = myDataSet.data.columns.map((val, idx) => {

                let t = {
                    date: moment(myDataSet.data.columns[idx]).format('YYYY')
                };

                indicators.forEach(indicator => {
                    t[indicator] = myDataSet.data.data[myDataSet.data.index.indexOf(indicator)][idx]
                });

                return t

            });

        }


        return returnData

    }

    getConfig() {


        const {indicators, dataSet, dataType, period} = this.props;

        if (dataSet) {
            //console.log(dataSet)
        }


        const myDataSet = dataSet[`${period}_${dataType}`];

        if (myDataSet) {
            return {

                chart: {
                    height:`${this.props.height - 80}px`,
                    width:`${this.props.width - 20}`,
                    type: this.props.chartType || 'line',
                    backgroundColor: {
                        linearGradient: {x1: 0, y1: 0, x2: 1, y2: 1},
                        stops: [
                            [0, styles.paper.backgroundColor],
                            [1, styles.paper.backgroundColor]
                        ]
                    },
                    style: {
                        fontFamily: '\'Unica One\', sans-serif'
                    },
                    plotBorderColor: styles.paper.backgroundColor
                },
                title: {
                    text: ''
                },

                yAxis: {
                    visible: true,
                    title: '',
                    labels: '',
                    plotBands: [{
                        color: red100, // Color value
                        from: 0, // Start of the plot band
                        to: -999 // End of the plot band
                    }]
                },

                xAxis: {
                    visible:false
                },
                series: indicators.map(indicator => {
                    return {
                        data: myDataSet.data.data[myDataSet.data.index.indexOf(indicator)],
                        name: indicator,
                        showInLegend:false
                    }
                })
            }
        }


        return {}
    }


    render() {

        //only render if data is found
        if (!this.props.dataSet) {
            return null;
        }


        return (

            <div style={{
                height:this.props.height,
                width:this.props.width

            }}>
                <ReactHighchart config={this.getConfig()}/>
            </div>



        );
    }
}

MiniChart.propTypes = {
    title: PropTypes.string,
    companyName: PropTypes.string,
    indicators: PropTypes.array,
    dataSet: PropTypes.object,
    dataType: PropTypes.oneOf(['standalone', 'consolidated']),
    period: PropTypes.oneOf(['annual', 'quarterly'])

};
MiniChart.defaultProps = {};

export default compose(withWidth())(MiniChart);
