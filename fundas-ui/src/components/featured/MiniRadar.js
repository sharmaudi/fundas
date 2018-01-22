import React, {Component} from 'react';
import PropTypes from 'prop-types';
import ReactHighchart from 'react-highcharts'
import {blue300, blue500, white} from "material-ui/styles/colors";
import {Link} from "react-router-dom";
import withWidth from "material-ui/utils/withWidth";
import compose from "recompose/compose";


const styles = {

    trial: {
        margin: 10,
        height: 400
    },
    paper: {
        backgroundColor: white,
        height: 350
    },
    div: {
        marginLeft: 'auto',
        marginRight: 'auto',
        width: '95%',
        height: 350
    },
    headerLiked: {
        color: white,
        backgroundColor: blue500,
        padding: 20
    },
    header: {
        color: white,
        backgroundColor: blue300,
        padding: 20
    },
    headerLink: {
        color: white,
        padding: 10,
        textDecoration: 'none'
    },
    checkbox: {
        float:'right'
    }
};

class MiniRadar extends Component {


    getConfig() {
        return {

            chart: {
                height:`${this.props.height - 80}px`,
                width:`${this.props.width}`,
                polar: true,
                type: 'line'
            },

            title: {
                text: '',
                marginTop: 0
            },


            xAxis: {
                visible:false,
                categories: this.props.metrics,
                tickmarkPlacement: 'on',
                lineWidth: 0
            },

            yAxis: {
                visible:false,
                gridLineInterpolation: 'polygon',
                lineWidth: 0,
                min: 0,
                max: 10
            },


            tooltip: {
                shared: true,
                pointFormat: '<span style="color:{series.color}">{series.name}: <b>{point.y:,.0f}</b><br/>'
            },



            series: [{
                name: 'Actual Scores',
                data: this.props.scores,
                type:'area',
                pointPlacement: 'on',
                color: blue500,
                showInLegend:false
            },
                {
                    name: 'Acceptable Scores',
                    data: this.props.acceptableScores,
                    pointPlacement: 'on',
                    color: 'grey',
                    dashStyle: 'Dot',
                    showInLegend:false
                }
            ]

        }
    }

    getHeader() {
        if(this.props.showLink) {
            return (
                <Link style={styles.headerLink} to={`/companies/${this.props.company}/analysis/${this.props.linkDataType}`}>
                    {this.props.company}
                </Link>
            )
        } else {
            return this.props.company
        }
    }

    render() {

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

MiniRadar.propTypes = {
    scores:PropTypes.array,
    acceptableScores:PropTypes.array,
    metrics:PropTypes.array,
    company:PropTypes.string,
    showLink:PropTypes.bool,
    linkDataType:PropTypes.string
};
MiniRadar.defaultProps = {};




export default compose(withWidth())(MiniRadar);
