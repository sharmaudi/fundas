import React, {Component} from 'react';
import PropTypes from 'prop-types';
import globalStyles from "../../styles";
import Radar from "../Radar";
import {Paper} from "material-ui";
import {typography} from "material-ui/styles/index";
import {cyan600, white} from "material-ui/styles/colors";
import Chart from "../Chart";
import MiniChart from "./MiniChart";

class PerformanceView extends Component {
    render() {
        const style ={
            paper: {
                minHeight: 50,
                minWidth: 50,
                height:350,
                width:350,
                margin: 20,
                textAlign: 'center',
            },
            title: {
                fontSize: 24,
                fontWeight: typography.fontWeightLight,
                backgroundColor: cyan600,
                color: white
            },
            progress: {
                padding: 20
            }



        };
        const featured = this.props.featured;
        const dataType = this.props.dataType || 'standalone';
        const company_list = dataType==='standalone'?featured.sort_order_standalone:featured.sort_order_consolidated;
        return (
            <div>
                <div style={globalStyles.section} className="row">


                    {company_list.map(company => {

                        const data = featured[company]['data'];

                        return (
                            <div key={company} className="col-xs-12 col-sm-6 col-md-6 col-lg-4 col-md m-b-15">
                                <Paper style={style.paper} zDepth={3}>
                                    <div style={style.title}>{company}</div>

                                    <MiniChart
                                        title={''}
                                        companyName={company}
                                        height={style.paper.height}
                                        width={style.paper.width}
                                        dataSet={data}
                                        dataType={dataType}
                                        period={'annual'}
                                        chartType='area'
                                        indicators={['SR', 'OP', 'NP']}

                                    />
                                </Paper>
                            </div>
                        )


                    })}
                </div>
            </div>
        );
    }
}

PerformanceView.propTypes = {
    featured:PropTypes.object,
    dataType:PropTypes.string
};
PerformanceView.defaultProps = {};

export default PerformanceView;
