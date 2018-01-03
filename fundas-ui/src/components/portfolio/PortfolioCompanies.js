import React, {Component} from 'react';
import compose from "recompose/compose";
import withWidth, {SMALL} from "material-ui/utils/withWidth";
import {connect} from "react-redux";
import Radar from "../Radar";


const style = {
    gridLarge: {
        display: 'grid',
        gridTemplateColumns: '1fr 1fr 1fr'
    },
    gridSmall: {
        display: 'grid',
        gridTemplateColumns: '1fr'
    }

};

class PortfolioCompanies extends Component {


    render() {

        const portfolio = this.props.portfolio

        if (!portfolio) {
            return (
                <div>Loading...</div>
            )
        }


        return (
            <div style={this.props.width === SMALL ? style.gridSmall : style.gridLarge}>
                {
                    Object.keys(portfolio.companies.standalone).map(e => {

                        let data = portfolio.companies.standalone[e];

                        return (
                            <Radar
                                showHeader={true}
                                key={e}
                                company={e}
                                scores={[data.performance, data.health, data.valuation, data.dividends]}
                                metrics={['performance', 'health', 'valuation', 'dividends']}
                                acceptableScores={[7, 6, 5, 3]}
                                showLink={true}
                                linkDataType={'standalone'}

                            />


                        )
                    })
                }

            </div>
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
