import React, {Component} from 'react';
import PropTypes from 'prop-types';
import ReactHighcharts from 'react-highcharts'
import {blue300, blue500, white} from "material-ui/styles/colors";
import {ResponsiveContainer} from "recharts";
import {Card, CardHeader, CardTitle, Checkbox} from "material-ui";
import {Link} from "react-router-dom";
import {connect} from "react-redux";
import withWidth from "material-ui/utils/withWidth";
import compose from "recompose/compose";
import {WATCHLIST_ADD, WATCHLIST_DELETE, WATCHLIST_LOAD} from "../constants/actionTypes";

import {watchlist} from "../agent";
import ActionFavorite from 'material-ui/svg-icons/action/favorite';
import ActionFavoriteBorder from 'material-ui/svg-icons/action/favorite-border';


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

class Radar extends Component {

    handleCheck(event, isInputChecked) {
        const {company} = this.props

        if(isInputChecked) {
            this.props.addToWatchlist(watchlist.addToWatchlist(company))
        } else {
            this.props.deleteFromWatchlist(watchlist.removeFromWatchlist(company))
        }


    }


    componentWillMount() {
        if(!this.props.watchlist) {
            this.props.loadWatchlist(watchlist.getWatchlist())
        }
    }

    getConfig() {
            return {

                chart: {
                    height: styles.div.height - 50,
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

        const {watchlist} = this.props;

        let checked = false;

        if(watchlist && watchlist.indexOf(this.props.company) > -1) {
            checked = true
        }

        return (
            <Card
                style={styles.trial}
            >


                    <CardHeader
                        style={checked?styles.headerLiked:styles.header}
                        title={this.getHeader()}
                    >


                </CardHeader>

                <CardTitle>
                    <Checkbox
                        checked={checked}
                        checkedIcon={<ActionFavorite />}
                        uncheckedIcon={<ActionFavoriteBorder />}
                        style={styles.checkbox}
                        onCheck={this.handleCheck.bind(this)}
                    />
                </CardTitle>



                <div style={styles.div}>
                    <ResponsiveContainer>
                        <ReactHighcharts
                            config={this.getConfig()}/>
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

const mapStateToProps = state => {
    return {
        featured: state.fundas.featured,
        watchlist: state.fundas.watchlist
    }
};


const mapDispatchToProps = dispatch => ({
    addToWatchlist: (payload) => dispatch({
        type: WATCHLIST_ADD,
        payload,
        skipTracking:false
    }),
    deleteFromWatchlist: (payload) => dispatch({
        type: WATCHLIST_DELETE,
        payload,
        skipTracking:false
    }),
    loadWatchlist: (payload) => dispatch({
        type: WATCHLIST_LOAD,
        payload,
        skipTracking:false
    }),
});

export default compose(withWidth(), connect(mapStateToProps, mapDispatchToProps))(Radar);
