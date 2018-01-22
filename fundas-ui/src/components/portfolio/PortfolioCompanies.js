import React, {Component} from 'react';
import compose from "recompose/compose";
import withWidth from "material-ui/utils/withWidth";
import {connect} from "react-redux";
import InfoView from "../featured/InfoView";



class PortfolioCompanies extends Component {


    render() {

        const portfolio = this.props.portfolio

        if (!portfolio) {
            return (
                <div>Loading...</div>
            )
        }


        return (
            <InfoView
             featured={portfolio.companies}
             dataType={'standalone'}
            />
        );
    }
}

PortfolioCompanies.propTypes = {};
PortfolioCompanies.defaultProps = {};

const mapStateToProps = state => {
    return {
        portfolio: state.fundas.portfolio
    }
};


const mapDispatchToProps = dispatch => ({});

export default compose(withWidth(), connect(mapStateToProps, mapDispatchToProps))(PortfolioCompanies);
