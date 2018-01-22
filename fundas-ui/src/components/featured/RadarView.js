import React, {Component} from 'react';
import PropTypes from 'prop-types';
import globalStyles from "../../styles";
import Radar from "../Radar";

class RadarView extends Component {
    render() {
        const featured = this.props.featured;
        const dataType = this.props.dataType || 'standalone';
        const company_list = dataType==='standalone'?featured.sort_order_standalone:featured.sort_order_consolidated;
        return (
            <div>
                <div style={globalStyles.section} className="row">


                    {company_list.map(company => {

                        const data = featured[company][`analysis_${dataType}`];

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
    }
}

RadarView.propTypes = {
    featured:PropTypes.object,
    dataType:PropTypes.string
};
RadarView.defaultProps = {};

export default RadarView;
