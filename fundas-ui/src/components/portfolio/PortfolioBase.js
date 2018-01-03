import React, {Component} from 'react';
import Subheader from "../Subheader";
import {CardActions, FlatButton} from "material-ui";
import Link from "react-router-dom/es/Link";
import globalStyles from "../../styles";
import PortfolioCompanies from "./PortfolioCompanies";
import PortfolioPerformance from "./PortfolioPerformance";
import Switch from "react-router-dom/es/Switch";
import Route from "react-router-dom/es/Route";
import compose from "recompose/compose";
import withWidth from "material-ui/utils/withWidth";
import {connect} from "react-redux";
import {PORTFOLIO_LOAD} from "../../constants/actionTypes";
import agent from "../../agent";

class PortfolioBase extends Component {

    componentWillMount() {
        if(!this.props.portfolio) {
            this.props.loadPortfolio(agent.companies.getPortfolio())
        }
    }

    render() {

        const {portfolio} = this.props;

        console.log("Portfolio:",portfolio);
        return (
            <div>
                <Subheader
                    title={"Portfolio"}
                    actions={(
                        <CardActions>
                            <div className="row">
                                <div className="col-lg-12 col-sm-6 col-xs-6">
                                    <FlatButton label="Companies" containerElement={<Link
                                        to={`/portfolio/companies`}/>}/>
                                    <FlatButton label="Performance" containerElement={<Link
                                        to={`/portfolio/performance`}/>}/>
                                </div>
                            </div>
                        </CardActions>
                    )}

                >
                    <div style={globalStyles.section}>
                        <Switch>

                            <Route path="/portfolio/companies" component={PortfolioCompanies}/>
                            <Route path="/portfolio/performance" component={PortfolioPerformance}/>

                            <Route path="/portfolio" component={PortfolioCompanies}/>


                        </Switch>
                    </div>

                </Subheader>



            </div>
        );
    }
}

PortfolioBase.propTypes = {};
PortfolioBase.defaultProps = {};

const mapStateToProps = state => {
    return {
        portfolio: state.fundas.portfolio
    }
};


const mapDispatchToProps = dispatch => ({
    loadPortfolio: (payload) => dispatch({
        type: PORTFOLIO_LOAD,
        payload,
        skipTracking: false
    })
});
export default compose(withWidth(), connect(mapStateToProps, mapDispatchToProps))(PortfolioBase);
