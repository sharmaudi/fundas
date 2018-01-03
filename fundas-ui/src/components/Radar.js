import React, {Component} from 'react';
import PropTypes from 'prop-types';
import ReactHighcharts from 'react-highcharts'
import {blue500, white} from "material-ui/styles/colors";
import {ResponsiveContainer} from "recharts";
import {Card, CardHeader} from "material-ui";
import {Link} from "react-router-dom";


const styles = {

    trial: {
        margin: 10,
        height: 500
    },
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
        backgroundColor: blue500,
        padding: 10
    },
    headerLink: {
        color: white,
        backgroundColor: blue500,
        padding: 10,
        textDecoration: 'none'
    }
};

class Radar extends Component {



    getConfig() {
            return {

                chart: {
                    polar: true,
                    type: 'line'
                },

                title: {
                    text: '',
                    marginTop: 0
                },


                xAxis: {
                    categories: this.props.metrics,
                    tickmarkPlacement: 'on',
                    lineWidth: 0
                },

                yAxis: {
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
                    color: blue500
                },
                    {
                        name: 'Acceptable Scores',
                        data: this.props.acceptableScores,
                        pointPlacement: 'on',
                        color: 'grey',
                        dashStyle: 'Dot'
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
            <Card
                style={styles.trial}
            >
                <CardHeader
                    title={this.getHeader()}
                >

                </CardHeader>

                <div style={styles.div}>
                    <ResponsiveContainer>
                        <ReactHighcharts config={this.getConfig()}/>
                    </ResponsiveContainer>
                </div>
            </Card>

        );
    }
}

Radar.propTypes = {
    scores:PropTypes.array,
    acceptableScores:PropTypes.array,
    metrics:PropTypes.array,
    company:PropTypes.string,
    showLink:PropTypes.bool,
    linkDataType:PropTypes.string
};
Radar.defaultProps = {};

export default Radar;
