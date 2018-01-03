import React, {Component} from 'react';
import PropTypes from 'prop-types';
import {blue50, white} from 'material-ui/styles/colors';


import ReactHighstock from 'react-highcharts/ReactHighstock'
import compose from "recompose/compose";
import withWidth from 'material-ui/utils/withWidth';

const styles = {
    paper: {
        backgroundColor: white,
        height: 800
    },
    div: {
        marginLeft: 'auto',
        marginRight: 'auto',
        width: '95%',
        height: 600
    },
    header: {
        color: white,
        backgroundColor: blue50,
        padding: 10
    }
};

class PriceChart extends Component {

    getConfig() {
        const momentum = this.props.momentumData;
        console.log("Momentum: ", momentum);
        let data = momentum.technicals.map(obj => [obj['date'], obj['close']]);
        let hhv52 = momentum.technicals.map(obj => [obj['date'], obj['hhv52']]);
        let hhvAllTime = momentum.technicals.map(obj => [obj['date'], obj['hhv_all_time']]);
        console.log("Data: ", data);
        return {
            chart: {
                height: styles.div.height
            },
            rangeSelector: {
                selected: 4
            },
            scrollbar: {
                enabled: false
            },
            title: {
                text: `${this.props.title} - Prices`
            },
            series: [{
                name: this.props.companyName,
                data: data,
                step: true,
                tooltip: {
                    valueDecimals: 2
                }
            },
                {
                    name: '52 week high',
                    data: hhv52,
                    tooltip: {
                        valueDecimals: 2
                    }
                },

                {
                    name: 'All time high',
                    data: hhvAllTime,
                    tooltip: {
                        valueDecimals: 2
                    }
                }
            ]
        };
    }


    getRocConfig() {
        const momentum = this.props.momentumData;
        let roc30 = momentum.technicals.map(obj => [obj['date'], obj['roc30']]);
        let roc60 = momentum.technicals.map(obj => [obj['date'], obj['roc60']]);
        return {
            chart: {
                height: styles.div.height / 2
            },
            rangeSelector: {
                selected: 4
            },
            title: {
                text: `${this.props.title} - Momentum`
            },
            scrollbar: {
                enabled: false
            },
            series: [
                {
                    name: 'ROC 30',
                    data: roc30,
                    tooltip: {
                        valueDecimals: 2
                    }
                },
                {
                    name: 'ROC60',
                    data: roc60,
                    tooltip: {
                        valueDecimals: 2
                    }
                }
            ]
        };
    }


    render() {

        if (!this.props.momentumData) {
            return null
        }

        return (

            <div>
                <ReactHighstock config={this.getConfig()}/>
                <ReactHighstock config={this.getRocConfig()}/>
            </div>


        );
    }
}

PriceChart.propTypes = {
    title: PropTypes.string,
    companyName: PropTypes.string,
    momentumData: PropTypes.object,
};
PriceChart.defaultProps = {};

export default compose(withWidth())(PriceChart);
