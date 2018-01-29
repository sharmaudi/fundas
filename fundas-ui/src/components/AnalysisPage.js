import React, {Component} from 'react';
import compose from "recompose/compose";
import {connect} from "react-redux";
import withWidth from "material-ui/utils/withWidth";
import Radar from "./Radar";
import Scores from "./Scores";
import ScreenerScores from "./ScreenerScores";


class AnalysisPage extends Component {

    render() {
        const {dataType} = this.props.match.params || 'standalone';
        const company = this.props.company;
        const categories = ['Valuation', 'Performance', 'Health', 'Dividends', 'Momentum'
        ];


        if (this.props.companyDataSet) {
            const analysisDataSet = this.props.companyDataSet.analysis[dataType];
            let screenerAnalysis = null;
            if(dataType === "standalone") {
                screenerAnalysis = this.props.companyDataSet.latest_standalone.analysis
            } else if(dataType === "consolidated") {
                screenerAnalysis = this.props.companyDataSet.latest_consolidated.analysis
            }

            console.log(screenerAnalysis);

            if (analysisDataSet) {
                const scores = [analysisDataSet.valuation.score,
                    analysisDataSet.performance.score,
                    analysisDataSet.health.score,
                    analysisDataSet.dividends.score,
                    analysisDataSet.momentum.score
                ];

                const acceptableScores = [5, 6, 6, 3, 6];
                return (

                    <div>

                    <div className="row">
                        <div className="col-xs-12 col-md-12 col-lg-12">

                                <Radar
                                    company={company}
                                    acceptableScores={acceptableScores}
                                    scores={scores}
                                    metrics={categories}
                                />

                        </div>
                    </div>


                    <div className="row">

                        <div className="col-xs-12 col-md-12 col-lg-12">

                            <ScreenerScores
                                title={"Screener Analysis"}
                                screenerAnalysis={screenerAnalysis}
                            >

                            </ScreenerScores>

                        </div>

                        <div className="col-xs-12 col-md-12 col-lg-12">

                            <Scores
                                title={"Performance Score"}
                                scores={analysisDataSet.performance.checks}
                                acceptableScore={6}
                                totalScore={analysisDataSet.performance.score}
                                company={company}
                            />

                        </div>

                        <div className="col-xs-12 col-md-12 col-lg-12">

                            <Scores
                                title={"Health Score"}
                                scores={analysisDataSet.health.checks}
                                acceptableScore={6}
                                totalScore={analysisDataSet.health.score}
                                company={company}
                            />

                        </div>

                        <div className="col-xs-12 col-md-12 col-lg-12">

                            <Scores
                                title={"Valuation Score"}
                                scores={analysisDataSet.valuation.checks}
                                acceptableScore={5}
                                totalScore={analysisDataSet.valuation.score}
                                company={company}
                            />

                        </div>

                        <div className="col-xs-12 col-md-12 col-lg-12">

                            <Scores
                                title={"Dividend Score"}
                                scores={analysisDataSet.dividends.checks}
                                acceptableScore={3}
                                totalScore={analysisDataSet.dividends.score}
                                company={company}
                            />

                        </div>

                        <div className="col-xs-12 col-md-12 col-lg-12">

                            <Scores
                                title={"Momentum Score"}
                                scores={analysisDataSet.momentum.checks}
                                acceptableScore={6}
                                totalScore={analysisDataSet.momentum.score}
                                company={company}
                            />

                        </div>

                    </div>

                    </div>

                );
            } else {
                return "No Data found"
            }
        } else {
            return "Loading..."
        }


    }
}

AnalysisPage.defaultProps = {};

const mapStateToProps = state => {
    return {
        company: state.fundas.company,
        companyDataSet: state.fundas.companyDataSet,
        companies: state.common.companies
    }
};

const mapDispatchToProps = dispatch => ({});

export default compose(withWidth(), connect(mapStateToProps, mapDispatchToProps))(AnalysisPage);
