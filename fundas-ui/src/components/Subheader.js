import React, {Component} from 'react';
import compose from "recompose/compose";
import withWidth from "material-ui/utils/withWidth";
import {Card, CardTitle} from 'material-ui/Card';
import PropTypes from 'prop-types';

class Subheader extends Component {
    render() {

        const {title, subtitle} = this.props;

        return (
            <Card>

                <div className="row">
                    <div className="col-lg-8">
                        <CardTitle title={title} subtitle={subtitle}>
                        </CardTitle>
                    </div>
                    <div className="col-lg-4" style={{float: 'right', paddingTop: 15}}>
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
