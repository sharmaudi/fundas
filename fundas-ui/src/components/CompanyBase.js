import React, {Component} from 'react';
import PropTypes from 'prop-types';
import agent from "../agent";
import compose from "recompose/compose";
import {connect} from "react-redux";
import {CHANGE_DATA_TYPE, COMPANY_LOAD} from "../constants/actionTypes";
import globalStyles from '../styles';
import {Route, Switch} from "react-router-dom";
import PerformancePage from "./PerformancePage";
import ValuationPage from "./ValuationPage";
import DividendsPage from "./DividendsPage";
import HealthPage from "./HealthPage"
import withWidth from 'material-ui/utils/withWidth';
import AnalysisPage from './AnalysisPage'
import Subheader from "./Subheader";
import MomentumPage from "./MomentumPage";
import {CardActions} from 'material-ui/Card';
import FlatButton from 'material-ui/FlatButton';
import Link from "react-router-dom/es/Link";
import {DropDownMenu, MenuItem} from "material-ui";

class CompanyBase extends Component {

    componentWillMount() {
        const companyInUrl = this.props.match.params.id;
        if (companyInUrl) {
            if (companyInUrl !== this.props.selectedCompany) {
                this.props.loadCompany(agent.companies.getCompany(companyInUrl), companyInUrl);
            }
        }
    }

    componentWillReceiveProps(nextProps) {
        if (this.props.match.params.id !== nextProps.match.params.id) {
            console.log("Reloading company");
            this.props.loadCompany(agent.companies.getCompany(nextProps.match.params.id), nextProps.match.params.id);
        }
    }

    render() {

        if (!this.props.selectedCompany) {
            return (<div>Loading...</div>)
        }

        let {chartType, dataType} = this.props.match.params;
        let {selectedCompany, companyDataSet} = this.props;
        chartType = chartType ? chartType : 'performance';
        dataType = dataType ? dataType : 'standalone';


        let companyName = selectedCompany;

        if (companyDataSet) {
            console.log("Company Data: ", companyDataSet);
            companyName = companyDataSet.company_info.nse_name ? companyDataSet.company_info.nse_name : companyDataSet.company_info.bse_name
        }

        return (

            <div>

                <Subheader
                    title={companyName}
                    subtitle={`NSE: ${companyDataSet.company_info.nse_code||'N/A'} | BSE: ${companyDataSet.company_info.bse_code||'N/A'}`}
                    dropdown={
                        (
                            <DropDownMenu value={dataType}>
                                <MenuItem label="Showing Standalone Figures"
                                          value='standalone'
                                          containerElement={<Link to={`/companies/${selectedCompany}/${chartType}/standalone`}/>}
                                          primaryText="Show Standalone Figures"/>
                                <MenuItem label="Showing Consolidated Figures"
                                          value='consolidated'
                                          containerElement={<Link to={`/companies/${selectedCompany}/${chartType}/consolidated`}/>}
                                          primaryText="Show Consolidated Figures" />
                            </DropDownMenu>
                        )
                    }
                    actions={(
                        <CardActions>
                            <FlatButton label="Info" containerElement={<Link
                                to={`/companies/${selectedCompany}/analysis/${dataType}`}/>}/>
                            <FlatButton label="Analysis" containerElement={<Link
                                to={`/companies/${selectedCompany}/analysis/${dataType}`}/>}/>
                            <FlatButton label="Performance" containerElement={<Link
                                to={`/companies/${selectedCompany}/performance/${dataType}`}/>}/>
                            <FlatButton label="Health" containerElement={<Link
                                to={`/companies/${selectedCompany}/health/${dataType}`}/>}/>
                            <FlatButton label="Valuation" containerElement={<Link
                                to={`/companies/${selectedCompany}/valuation/${dataType}`}/>}/>
                            <FlatButton label="Dividends" containerElement={<Link
                                to={`/companies/${selectedCompany}/dividends/${dataType}`}/>}/>
                            <FlatButton label="Momentum" containerElement={<Link
                                to={`/companies/${selectedCompany}/momentum/${dataType}`}/>}/>

                        </CardActions>
                    )}

                />

                <div style={globalStyles.section}>
                    <Switch>

                        <Route path="/companies/:id/performance/:dataType" component={PerformancePage}/>
                        <Route path="/companies/:id/performance" component={PerformancePage}/>


                        <Route path="/companies/:id/health/:dataType" component={HealthPage}/>
                        <Route path="/companies/:id/health" component={HealthPage}/>

                        <Route path="/companies/:id/valuation/:dataType" component={ValuationPage}/>
                        <Route path="/companies/:id/valuation" component={ValuationPage}/>

                        <Route path="/companies/:id/dividends/:dataType" component={DividendsPage}/>
                        <Route path="/companies/:id/dividends" component={DividendsPage}/>

                        <Route path="/companies/:id/analysis/:dataType" component={AnalysisPage}/>
                        <Route path="/companies/:id/analysis" component={AnalysisPage}/>

                        <Route path="/companies/:id/momentum/:dataType" component={MomentumPage}/>
                        <Route path="/companies/:id/momentum" component={MomentumPage}/>

                        <Route path="/companies/:id" component={PerformancePage}/>
                    </Switch>
                </div>
            </div>

        );
    }
}

const mapStateToProps = state => {
    return {
        companyDataSet: state.fundas.companyDataSet,
        selectedCompany: state.fundas.company
    }
};


const mapDispatchToProps = dispatch => ({
    loadCompany: (payload, company) => dispatch({
        type: COMPANY_LOAD,
        payload,
        company,
        skipTracking: false
    }),
    changeDataType: (newDataType) => dispatch({
        type: CHANGE_DATA_TYPE,
        payload: {
            dataType: newDataType
        }
    })
});

CompanyBase.propTypes = {
    company: PropTypes.string
};
CompanyBase.defaultProps = {};

export default compose(withWidth(), connect(mapStateToProps, mapDispatchToProps))(CompanyBase);
