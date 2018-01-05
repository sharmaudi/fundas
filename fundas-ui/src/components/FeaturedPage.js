import React, {Component} from 'react';
import agent, {watchlist} from "../agent";
import compose from "recompose/compose";
import {connect} from "react-redux";
import {
    CHANGE_DATA_TYPE, FEATURED_LOAD, WATCHLIST_ADD, WATCHLIST_DELETE,
    WATCHLIST_LOAD
} from "../constants/actionTypes";
import globalStyles from '../styles';
import MenuItem from 'material-ui/MenuItem';
import {DropDownMenu, Toolbar, ToolbarGroup} from "material-ui";
import {store} from "../store";
import {push} from "react-router-redux";
import {Link} from "react-router-dom";
import {blue500, white} from "material-ui/styles/colors";
import withWidth from 'material-ui/utils/withWidth';
import Radar from "./Radar";
import {typography} from "material-ui/styles/index";
import Subheader from "./Subheader";


const styles = {
    title: {
        fontSize: 24,
        fontWeight: typography.fontWeightMedium,
        color: white,
        backgroundColor: blue500,
        padding: 20,
        margin:20

    },
    toolbarItem: {

    }
};

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

    getToolbarElements() {
        let {dataType} = this.props.match.params;
        dataType = dataType ? dataType : 'standalone';


        return (
            <Toolbar style={globalStyles.toolbar} >

                <ToolbarGroup
                    firstChild={true}
                    style={styles.toolbarItem}
                >

                    <MenuItem value={'standalone'}
                              style={dataType === 'standalone' ? (globalStyles.toolbarActive) : globalStyles.toolbarInactive}
                              primaryText="Standalone"
                              containerElement={<Link
                                  to={`/featured/standalone`}/>}
                    />
                    <MenuItem value={'consolidated'}
                              style={dataType === 'consolidated' ? (globalStyles.toolbarActive) : globalStyles.toolbarInactive}
                              primaryText="Consolidated"
                              containerElement={<Link
                                  to={`/featured/consolidated`}/>}
                    />


                </ToolbarGroup>


            </Toolbar>
        )
    }

    render() {

        const featured = this.props.featured;
        const dataType = this.props.match.params.dataType || 'standalone';
        if(featured) {

            const company_list = dataType==='standalone'?featured.standalone_list:featured.consolidated_list;
            return (

                <div >
                    <Subheader
                        title='Featured Companies'
                        subtitle={`Updated weekly`}
                        dropdown={
                            (
                                <DropDownMenu value={dataType}>
                                    <MenuItem label="Showing Standalone Results"
                                              value='standalone'
                                              containerElement={<Link to={`/featured/standalone`}/>}
                                              primaryText="Show Standalone Results"/>
                                    <MenuItem label="Showing Consolidated Results"
                                              value='consolidated'
                                              containerElement={<Link to={`/featured/consolidated`}/>}
                                              primaryText="Show Consolidated Results" />
                                </DropDownMenu>
                            )
                        }


                    />

                    <div style={globalStyles.section} className="row">


                    {company_list.map(company => {

                        const data = featured[dataType][company];

                        return (
                            <div key={company} className="col-xs-12 col-sm-6 col-md-6 col-lg-4 col-md m-b-15">
                            <Radar
                                showHeader={true}
                                key={company}
                                company={company}
                                scores={[data.performance, data.health, data.valuation, data.dividends]}
                                metrics={['performance','health', 'valuation', 'dividends']}
                                acceptableScores={[7,6,5,3]}
                                showLink={true}
                                linkDataType={dataType}
                                showAddFavorite={true}
                                watchlist={this.props.watchlist}

                            />
                            </div>
                        )


                    })}
                    </div>
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
    return {
        featured: state.fundas.featured,
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
        skipTracking:false
    }),
    addToWatchlist: (payload) => dispatch({
        type: WATCHLIST_ADD,
        payload,
        skipTracking:false
    }),
    deleteFromWatchlist: (payload) => dispatch({
        type: WATCHLIST_DELETE,
        payload,
        skipTracking:false
    })
});

FeaturedPage.propTypes = {};
FeaturedPage.defaultProps = {};

export default compose(withWidth(), connect(mapStateToProps, mapDispatchToProps))(FeaturedPage);
