import React, {Component} from 'react';
import agent, {watchlist} from "../../agent";
import compose from "recompose/compose";
import {connect} from "react-redux";
import {
    CHANGE_DATA_TYPE, FEATURED_LOAD, WATCHLIST_ADD, WATCHLIST_DELETE,
    WATCHLIST_LOAD
} from "../../constants/actionTypes";
import {store} from "../../store";
import {push} from "react-router-redux";
import withWidth from 'material-ui/utils/withWidth';
import Subheader from "../Subheader";
import InfoView from "./InfoView";


class FeaturedPage extends Component {


    loadCompany() {

    }

    componentWillMount() {
        this.props.loadFeatured(agent.companies.getFeatured());
        this.props.loadWatchlist(watchlist.getWatchlist())
    }


    handleChangeChart(event, key, value) {
        let dataType = this.props.match.params.dataType;
        dataType = dataType || 'standalone';
        store.dispatch(push(`/companies/${this.props.selectedCompany}/${value}/${dataType}`))
    }


    handleChangeDataType(event, key, value) {
        const chartType = this.props.match.params.chartType;
        store.dispatch(push(`/companies/${this.props.selectedCompany}/${chartType}/${value}`))
    }


    render() {

        const featured = this.props.featured;
        const dataType = this.props.match.params.dataType || 'standalone';
        const pageType = this.props.match.params.pageType || 'analysis';

        console.log(`Page Type : ${pageType}`);

        let slideIndex = 1;
        if (pageType === "info") {
            slideIndex = 0
        } else if (pageType === "performance") {
            slideIndex = 2
        } else if (pageType === "analysis") {
            slideIndex = 1
        }


        if (featured) {

            return (

                <div>
                    <Subheader
                        title='Featured Companies'
                        subtitle={`Updated weekly`}

                    >
                        <InfoView
                            featured={featured}
                            dataType={dataType}
                            slideIndex={slideIndex}
                            perPage={15}
                        />
                    </Subheader>
                </div>

            );
        } else {
            return (
                <div>
                    Loading...
                </div>
            )
        }


    }
}

const mapStateToProps = state => {
    let featured = state.fundas.featured;
    return {
        featured: featured,
        watchlist: state.fundas.watchlist
    }
};


const mapDispatchToProps = dispatch => ({
    loadFeatured: (payload) => dispatch({
        type: FEATURED_LOAD,
        payload,
        skipTracking: false
    }),
    changeDataType: (newDataType) => dispatch({
        type: CHANGE_DATA_TYPE,
        payload: {
            dataType: newDataType
        }
    }),
    loadWatchlist: (payload) => dispatch({
        type: WATCHLIST_LOAD,
        payload,
        skipTracking: false
    }),
    addToWatchlist: (payload) => dispatch({
        type: WATCHLIST_ADD,
        payload,
        skipTracking: false
    }),
    deleteFromWatchlist: (payload) => dispatch({
        type: WATCHLIST_DELETE,
        payload,
        skipTracking: false
    })
});

FeaturedPage.propTypes = {};
FeaturedPage.defaultProps = {};

export default compose(withWidth(), connect(mapStateToProps, mapDispatchToProps))(FeaturedPage);
