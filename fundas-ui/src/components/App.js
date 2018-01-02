import React, {Component} from 'react';
import PropTypes from 'prop-types';

import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import LeftDrawer from './LeftDrawer'
import withWidth, {LARGE, SMALL} from 'material-ui/utils/withWidth';
import ThemeDefault from '../theme-default';
import Header from './Header'
import Config from "../Config";
import config from "../Config";
import compose from 'recompose/compose';
import {connect} from 'react-redux';
import {APP_LOAD, REDIRECT} from '../constants/actionTypes';
import {store} from '../store';
import agent from '../agent';
import {Route, Switch} from 'react-router-dom';


import {push} from 'react-router-redux'
import DashboardPage from "./DashboardPage";
import CompanyBase from "./CompanyBase";
import HighchartsMore from 'highcharts-more';
import ReactHighcharts from 'react-highcharts'
import FeaturedPage from "./FeaturedPage";
import {Snackbar} from "material-ui";

HighchartsMore(ReactHighcharts.Highcharts);

class App extends Component {

    constructor(props) {
        super(props);
        this.state = {
            navDrawerOpen: false
        }
    }

    componentWillReceiveProps(nextProps) {
        if (this.props.width !== nextProps.width) {
            this.setState({navDrawerOpen: nextProps.width === LARGE});
        }

        if (nextProps.redirectTo) {
            store.dispatch(push(nextProps.redirectTo));
            this.props.onRedirect();
        }
    }


    componentWillMount() {
        const companies = window.localStorage.getItem(config.keys.ALL_COMPANIES);
        if(companies) {
            this.props.onLoad( null, companies);
        } else {
            this.props.onLoad( agent.companies.all(), companies);
        }
    }

    handleChangeRequestNavDrawer() {
        this.setState((prevState) => {
            return {navDrawerOpen: !prevState.navDrawerOpen}
        });
    }


    handleOnSelect(str, idx){
        console.log('Router Props: ',this.props);

        const currentPath = this.props.location.pathname;

        let arr = currentPath.split('/');

        let newLocation = `/companies/${this.props.companies[idx]}`;

        let append = 'performance/standalone';
        if(arr.length > 3) {
            append =  arr.slice(3).join('/')
        }

        console.log('Append is '+ append);

        newLocation = newLocation + '/' + append;


        if(idx !== -1 ) {
            store.dispatch(push(newLocation))
        }
    };


    render() {

        let {navDrawerOpen} = this.state;
        let {companies} = this.props;
        const paddingLeftDrawerOpen = 220;
        let company = this.props.match.params.id;

        console.log(`Company is ${company}`);

        const styles = {
            header: {
                paddingLeft: navDrawerOpen ? paddingLeftDrawerOpen : 0,
                marginLeft:0
            },
            container: {
                overflowX:'hidden',
                marginTop: '70px',
                paddingLeft: navDrawerOpen && this.props.width !== SMALL ? paddingLeftDrawerOpen : 5
            }
        };


        if (this.props.appLoaded) {
            return (
                <MuiThemeProvider muiTheme={ThemeDefault}>

                        <Header styles={styles.header}
                                handleChangeRequestNavDrawer={this.handleChangeRequestNavDrawer.bind(this)}
                                data={companies}
                                handleOnSelect={this.handleOnSelect.bind(this)}

                        />

                        <LeftDrawer navDrawerOpen={navDrawerOpen}
                                    menus={Config.menus}
                                    company={this.props.company}
                                    username="User Admin"/>

                        {/*<div style={styles.container}>*/}
                            {/*{this.props.children}*/}
                        {/*</div>*/}

                        <div style={styles.container}>
                            <Switch>
                                <Route path="/Dashboard" component={DashboardPage}/>
                                <Route path="/featured/:dataType" component={FeaturedPage}/>
                                <Route path="/companies/:id/:chartType/:dataType" component={CompanyBase}/>
                                <Route path="/companies/:id/:chartType" component={CompanyBase}/>
                                <Route path="/companies/:id/" component={CompanyBase}/>
                                <Route path="/" component={DashboardPage}/>
                            </Switch>
                        </div>

                        <Snackbar
                            open={this.props.asyncPending}
                            message="Fetching..."
                            autoHideDuration={4000}
                            onRequestClose={this.handleRequestClose}
                        />






                </MuiThemeProvider>

            );
        } else {
            return <MuiThemeProvider muiTheme={ThemeDefault}>
                <div>
                    {this.props.error && (<p>Error while initializing application.</p>)}
                    {!this.props.error && (<p>Loading...</p>)}
                </div>
            </MuiThemeProvider>
        }


    }
}

App.propTypes = {
    children: PropTypes.element,
    width: PropTypes.number
};

const mapStateToProps = state => {
    return {
        appLoaded: state.common.appLoaded,
        appName: state.common.appName,
        currentUser: state.common.currentUser,
        redirectTo: state.common.redirectTo,
        error: state.common.error,
        companies: state.common.companies,
        company:state.fundas.company,
        asyncPending:state.common.asyncPending
    }};

const mapDispatchToProps = dispatch => ({
    onLoad: (payload, companies) =>
        dispatch({ type: APP_LOAD, payload, companies, skipTracking: false }),
    onRedirect: () =>
        dispatch({ type: REDIRECT })
});

export default compose(withWidth(), connect(mapStateToProps, mapDispatchToProps))(App);