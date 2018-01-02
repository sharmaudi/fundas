import React, {Component} from 'react';
import compose from "recompose/compose";
import withWidth from "material-ui/utils/withWidth";
import {Card, CardTitle} from 'material-ui/Card';
import PropTypes from 'prop-types';
import {blue500, white} from "material-ui/styles/colors";


const styles = {

    trial: {
        margin: 10
    },
    paper: {
        backgroundColor: white,
        height: 400
    },
    div: {
        marginLeft: 'auto',
        marginRight: 'auto',
        width: '95%',
        height: 350
    },
    header: {
        color: white,
        backgroundColor: blue500,
        padding: 10
    },
    headerLink: {
        color: white,
        backgroundColor: blue500,
        padding: 10,
        textDecoration: 'none'
    }
};

class Subheader extends Component {
    render() {

        const {title, subtitle} = this.props;

        return (
            <Card style={styles.trial}>

                <div className="row">
                    <div className="col-lg-8 col-sm-12 col-xs-12">
                        <CardTitle title={title} subtitle={subtitle}>
                        </CardTitle>
                    </div>
                    <div className="col-lg-4 col-sm-12 col-xs-12">
                        <div className="row">
                            <div className="col-lg-4"> {this.props.dropdown}</div>

                        </div>
                    </div>

                </div>

                {this.props.actions}

            </Card>
        )
    }
}

Subheader.propTypes = {
    title: PropTypes.string,
    subtitle: PropTypes.string,
    actions: PropTypes.object
};
Subheader.defaultProps = {};

export default compose(withWidth())(Subheader);
