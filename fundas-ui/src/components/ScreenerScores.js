import React, {Component} from 'react';
import PropTypes from 'prop-types';
import {Paper} from "material-ui";
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
        margin: 10
    },
    itemChart: {
        textAlign: 'center',
        order: 1,
        flex: '2'
    },
    itemListSmall: {
        order: 1,
        flex: '1'

    },
    itemChartSmall: {
        textAlign: 'center',
        order: 2,
        flex: '1'
    },
    success: {
        backgroundColor: green200,
        fontWeight: typography.fontWeightNormal,

    },
    failure: {
        backgroundColor: red200,
        fontWeight: typography.fontWeightNormal,

        color: 'white'
    }, successSmall: {
        backgroundColor: green200,
        fontWeight: typography.fontWeightLight,
        fontSize: '.8em',

    },
    failureSmall: {
        backgroundColor: red200,
        color: 'white',
        fontWeight: typography.fontWeightLight,
        fontSize: '.7em',
    },
    subtextSmall: {
        fontWeight: typography.fontWeightLight,
        fontSize: '.5em'
    },
    title: {
        fontSize: 24,
        fontWeight: typography.fontWeightMedium,
        color: white,
        backgroundColor: blue500,
        padding: 10,
        margin: 0
    },
};

class ScreenerScores extends Component {


    getGoodItems(obj) {


        console.log("Getting good items:", obj);
        return obj.good.map((val, idx) => {


                if (this.props.width === SMALL) {
                    return (
                        <ListItem key={idx}
                                  primaryText={val}
                                  style={flexStyles.successSmall}
                        />
                    )
                } else {
                    return (
                        <ListItem key={idx}
                                  primaryText={val}
                                  style={flexStyles.success}
                                  leftIcon={<ActionThumbUp/>}
                        />
                    )
                }

            }
        )
    }

    getBadItems(obj) {
        console.log("Getting bad items:", obj);
        return obj.bad.map((val, idx) => {


                if (this.props.width === SMALL) {
                    return (
                        <ListItem key={idx}
                                  primaryText={val}
                                  style={flexStyles.failureSmall}
                        />
                    )
                } else {
                    return (
                        <ListItem key={idx}
                                  primaryText={val}
                                  style={flexStyles.failure}
                                  leftIcon={<ActionThumbDown/>}
                        />
                    )
                }

            }
        )
    }

    render() {

        const {screenerAnalysis, width} = this.props;

        if (!screenerAnalysis) {
            return null
        }

        return (

            <Paper style={flexStyles.itemPaper}>

                <div style={flexStyles.title}>{this.props.title}</div>
                <div style={width === SMALL ? flexStyles.containerSmall : flexStyles.container}>

                    <div style={width === SMALL ? flexStyles.itemListSmall : flexStyles.itemList}>


                        <List style={{padding: 0}}>
                            {this.getGoodItems(screenerAnalysis)}
                            {this.getBadItems(screenerAnalysis)}
                        </List>


                    </div>
                </div>
            </Paper>


        );
    }
}

ScreenerScores.propTypes = {
    title: PropTypes.string,
    screenerAnalysis: PropTypes.object
};
ScreenerScores.defaultProps = {};

export default compose(withWidth())(ScreenerScores);



