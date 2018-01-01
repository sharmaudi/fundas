import React, {Component} from 'react';
import PropTypes from 'prop-types';
import {CircularProgress, Paper} from "material-ui";
import {List, ListItem} from 'material-ui/List';
import ActionThumbUp from "material-ui/svg-icons/action/thumb-up"
import ActionThumbDown from "material-ui/svg-icons/action/thumb-down"
import {typography} from "material-ui/styles/index";
import {blue500, green200, red200, white} from "material-ui/styles/colors";
import compose from "recompose/compose";
import withWidth, {SMALL} from "material-ui/utils/withWidth";


const flexStyles = {
    container: {
        display: 'flex',
        flexFlow: 'row wrap',
        fontWeight: 'bold',
        textAlign: 'left',
        alignItems: 'center',
        justifyContent: 'center',
    },
    containerSmall: {
        display: 'flex',
        flexFlow: 'row wrap',
        fontWeight: 'bold',
        textAlign: 'left',
        alignItems: 'center',
        justifyContent: 'center',
    },
    itemList: {
        order: 1,
        flex: '4'

    },
    itemPaper: {
        margin:10
    },
    itemChart: {
        textAlign:'center',
        order: 1,
        flex: '2'
    },
    itemListSmall: {
        order: 1,
        flex: '1'

    },
    itemChartSmall: {
        textAlign:'center',
        order: 2,
        flex: '1'
    },
    success:{
        backgroundColor:green200,
        fontWeight: typography.fontWeightNormal,

    },
    failure:{
        backgroundColor:red200,
        fontWeight: typography.fontWeightNormal,

        color:'white'
    },successSmall:{
        backgroundColor:green200,
        fontWeight: typography.fontWeightLight,
        fontSize:'.8em',

    },
    failureSmall:{
        backgroundColor:red200,
        color:'white',
        fontWeight: typography.fontWeightLight,
        fontSize:'.7em',
    },
    subtextSmall: {
        fontWeight: typography.fontWeightLight,
        fontSize:'.5em'
    },
    title: {
        fontSize: 24,
        fontWeight: typography.fontWeightMedium,
        color: white,
        backgroundColor: blue500,
        padding: 10,
        margin:0
    },
};

class Scores extends Component {


    round(val) {
        return Math.round(val * 100) / 100
    }


    getSecondaryText(scoreObj) {
        let span1 = null;
        let span2 = null;
        if (scoreObj.lcol) {


            if(this.props.width === SMALL) {
                span1 = span1 = (<span style={flexStyles.subtextSmall}>{scoreObj.lcol} = {this.round(scoreObj.lhs)}</span>)
            } else {
                span1 = (<span>{scoreObj.lcol} = {this.round(scoreObj.lhs)}</span>)
            }

        }

        if (scoreObj.rcol) {
            if(this.props.width === SMALL) {
                span2 = (<span style={flexStyles.subtextSmall}>&nbsp;|&nbsp;{scoreObj.rcol} = {this.round(scoreObj.rhs)}</span>)
            } else {
                span2 = (<span>&nbsp;|&nbsp;{scoreObj.rcol} = {this.round(scoreObj.rhs)}</span>)
            }
        }

        return <div>
            {span1}
            {span2}
        </div>

    }

    getListItem(scoreObj) {
        if(this.props.width === SMALL) {
            return <ListItem key={scoreObj.id}
                             primaryText={scoreObj.rule}
                             secondaryText={this.getSecondaryText(scoreObj)}
                             style={scoreObj.outcome ? flexStyles.successSmall : flexStyles.failureSmall}

            />
        } else {
            return <ListItem key={scoreObj.id}
                      primaryText={scoreObj.rule}
                      secondaryText={this.getSecondaryText(scoreObj)}
                      leftIcon={scoreObj.outcome?<ActionThumbUp/>:<ActionThumbDown/>}
                      style={scoreObj.outcome ? flexStyles.success : flexStyles.failure}

            />
        }
    }

    render() {

        const {totalScore, acceptableScore,width} = this.props;
        let color = 'green';

        if (totalScore < 8 && totalScore >= acceptableScore) {
            color = 'yellow'
        }

        if (totalScore < acceptableScore) {
            color = 'red'
        }

        return (

            <Paper style={flexStyles.itemPaper}>

                <div style={flexStyles.title}>{this.props.title}</div>
                <div style={width === SMALL?flexStyles.containerSmall:flexStyles.container}>

                    <div style={width === SMALL?flexStyles.itemListSmall:flexStyles.itemList}>


                        {this.props.scores &&


                        <List style={{padding:0}}>
                            {this.props.scores.map(scoreObj =>
                                (

                                    this.getListItem(scoreObj)
                                )
                            )}
                        </List>

                        }




                    </div>
                    <div style={width === SMALL?flexStyles.itemChartSmall:flexStyles.itemChart}>

                        <h1>{totalScore}/10</h1>

                        <Progress
                            color={color}
                            progress={totalScore}
                        />


                    </div>
                </div>
            </Paper>


        );
    }
}

Scores.propTypes = {
    scores: PropTypes.array,
    title: PropTypes.string,
    company: PropTypes.string,
    totalScore: PropTypes.number
};
Scores.defaultProps = {};

export default compose(withWidth())(Scores);


const Progress = ({progress, color}) => (
        <div>

            <CircularProgress
                style={{
                    verticalAlign: 'middle'
                }}
                color={color}
                mode="determinate"
                max={10}
                min={0}
                value={progress}
                size={200}
                thickness={10}
            />
    </div>
);


