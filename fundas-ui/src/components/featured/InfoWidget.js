import React from 'react';
import {Tab, Tabs} from 'material-ui/Tabs';
// From https://github.com/oliviertassinari/react-swipeable-views
import SwipeableViews from 'react-swipeable-views';
import MiniChart from "./MiniChart";
import {typography} from "material-ui/styles/index";
import {cyan600, white} from "material-ui/styles/colors";
import MiniRadar from "./MiniRadar";
import Assessment from "material-ui/svg-icons/action/assessment"
import Info from "material-ui/svg-icons/action/info"
import Timeline from "material-ui/svg-icons/action/timeline"



const styles = {
    headline: {
        fontSize: 24,
        paddingTop: 16,
        marginBottom: 12,
        fontWeight: 400,
    },
    slide: {
        padding: 10,
        overflowX: 'hidden'

},paper: {
        minHeight: 50,
        minWidth: 50,
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



export default class InfoWidget extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            slideIndex: props.slideIndex || 1,
        };
    }

    handleChange = (value) => {
        this.setState({
            slideIndex: value,
        });
    };

    componentWillReceiveProps(nextProps) {
        if (this.state.slideIndex !== nextProps.slideIndex) {
            this.setState({
                slideIndex:nextProps.slideIndex
            })
        }
    }

    render() {

        const {company,featured,dataType} = this.props;
        const data = featured[company]['data'];
        const scores = featured[company][`analysis_${dataType}`];


        return (
            <div>
                <Tabs
                    onChange={this.handleChange}
                    value={this.state.slideIndex}
                >
                    <Tab icon={<Info/>} value={0} />
                    <Tab icon={<Assessment/>} value={1} />
                    <Tab icon={<Timeline/>} value={2} />
                </Tabs>
                <SwipeableViews
                    index={this.state.slideIndex}
                    onChangeIndex={this.handleChange}
                >
                    <div>
                        <h2 style={styles.headline}>Tabs with slide effect</h2>
                        Swipe to see the next slide.<br />
                    </div>

                    <div style={styles.slide}>
                        <MiniRadar
                            showHeader={true}
                            key={company}
                            company={company}
                            height={this.props.height - 50}
                            width={this.props.width}
                            scores={[scores.performance, scores.health, scores.valuation, scores.dividends, scores.momentum]}
                            metrics={['performance','health', 'valuation', 'dividends', 'momentum']}
                            acceptableScores={[7,6,5,3,8]}
                            showLink={true}
                            linkDataType={dataType}
                        />
                    </div>
                    <div style={styles.slide}>
                        <MiniChart
                            title={''}
                            companyName={company}
                            dataSet={data}
                            dataType={dataType}
                            height={this.props.height - 50}
                            width={this.props.width}
                            period={'annual'}
                            chartType='area'
                            indicators={['SR', 'OP', 'NP']}

                        />
                    </div>
                </SwipeableViews>
            </div>
        );
    }
}