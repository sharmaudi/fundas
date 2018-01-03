import React, {Component} from 'react';
import compose from "recompose/compose";
import {connect} from "react-redux";
import withWidth from "material-ui/utils/withWidth";
import {MOMENTUM_LOAD} from "../constants/actionTypes";
import agent from "../agent";
import PriceChart from "./PriceChart";

class MomentumPage extends Component {

    componentWillMount() {

        const selectedCompany = this.props.company;

        if(selectedCompany) {
            if(!this.props.momentum) {
                this.props.loadMomentum(agent.companies.getMomentum(selectedCompany));
            }

            if(this.props.momentum && this.props.momentum.Company !== selectedCompany) {
                this.props.loadMomentum(agent.companies.getMomentum(selectedCompany));
            }

        }
    }

    render() {


        if (this.props.momentum) {
            return (
                    <div>
                        <PriceChart
                        title={this.props.company}
                        companyName={this.props.company}
                        momentumData={this.props.momentum}
                        />
                    </div>
            )
        } else {
            return "Loading..."
        }


    }
}

MomentumPage.defaultProps = {};

const mapStateToProps = state => {
    return {
        company: state.fundas.company,
        companyDataSet: state.fundas.companyDataSet,
        companies: state.common.companies,
        momentum: state.fundas.momentum
    }
};

const mapDispatchToProps = dispatch => ({
    loadMomentum: (payload) => dispatch({
        type: MOMENTUM_LOAD,
        payload,
        skipTracking: false
    })
});

export default compose(withWidth(), connect(mapStateToProps, mapDispatchToProps))(MomentumPage);
