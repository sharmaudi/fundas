import React, {Component} from 'react';
import PropTypes from 'prop-types';
import Paper from 'material-ui/Paper';
import {blue50, white} from 'material-ui/styles/colors';
import {CartesianGrid, Legend, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis} from 'recharts';
import GlobalStyles from '../styles';
import moment from 'moment'

import ReactHighchart from 'react-highcharts'
import compose from "recompose/compose";
import withWidth, {SMALL} from 'material-ui/utils/withWidth';

const styles = {
    paper: {
        backgroundColor: white,
        height: 400
    },
    div: {
        marginLeft: 'auto',
        marginRight: 'auto',
        width: '95%',
        height: 350
    },
    header: {
        color: white,
        backgroundColor: blue50,
        padding: 10
    }
};
class Chart extends Component {

    createData() {
        const { indicators, dataSet, dataType, period} = this.props;

        if(dataSet) {
            //console.log(dataSet)
        }


        const myDataSet = dataSet[`${period}_${dataType}`];
        let returnData = [];

        if(myDataSet) {
            console.log(myDataSet);

            returnData = myDataSet.data.columns.map( (val, idx) => {

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


        const { indicators, dataSet, dataType, period, width} = this.props;

        if(dataSet) {
            //console.log(dataSet)
        }


        const myDataSet = dataSet[`${period}_${dataType}`];

        if(myDataSet) {
            return {

                chart: {
                    type: this.props.chartType||'line',
                    backgroundColor: {
                        linearGradient: { x1: 0, y1: 0, x2: 1, y2: 1 },
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
                    text: this.props.title
                },

                yAxis: {
                    visible: width === SMALL?false:true
                },

                xAxis: {
                    categories: myDataSet.data.columns.map(d => moment(d).format('MMM-YYYY'))
                },
                series: indicators.map(indicator => {
                    return {
                        data: myDataSet.data.data[myDataSet.data.index.indexOf(indicator)],
                        name: indicator
                    }
                })
            }
        }



        return {}
    }


    getColor(idx) {
        const list = [
            '#caff70',
            '#a579ca',
            '#4ca64c',
            '#8884d8',
            '#ffffff',
            '#00ced1',
            '#6666cc',
            '#e93cac',
            '#d4dfda'
        ];

        return list[idx]
    }

    getLines() {
        return this.props.indicators.map((i, idx) =>
            (<Line type="monotone" dataKey={i} stroke={this.getColor(idx)} />)
        )
    }

    getChart() {
        const type = this.props.chartType;
        const data = this.createData();
        if(!type || type === 'line') {
            return (
                <LineChart width={730} height={250} data={data}
                           margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <XAxis dataKey="date" stroke="none" tick={{fill: white}}/>
                    {this.getLines()}
                </LineChart>
            )
        }


    }
    render() {

        //only render if data is found
        if(!this.props.dataSet) {
            return null;
        }


        return (
            <div style={GlobalStyles.section}>

                <Paper style={styles.paper}>
                    {/*<div style={{...GlobalStyles.title, ...styles.header}}>{this.props.title}</div>*/}
                    <div style={styles.div}>
                        <ResponsiveContainer>
                            <ReactHighchart config={this.getConfig()}/>
                        </ResponsiveContainer>
                    </div>
                </Paper>

            </div>

        );
    }
}

Chart.propTypes = {
    title:PropTypes.string,
    companyName:PropTypes.string,
    indicators: PropTypes.array,
    dataSet: PropTypes.object,
    dataType:PropTypes.oneOf(['standalone','consolidated']),
    period:PropTypes.oneOf(['annual','quarterly'])

};
Chart.defaultProps = {};

export default compose(withWidth())(Chart);
