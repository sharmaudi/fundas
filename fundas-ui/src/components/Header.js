import React from 'react';
import PropTypes from 'prop-types';
import AppBar from 'material-ui/AppBar';
import IconButton from 'material-ui/IconButton';
import Menu from 'material-ui/svg-icons/navigation/menu';
import {white} from 'material-ui/styles/colors';
import SearchBox from './SearchBox';

class Header extends React.Component {

    render() {
        const {styles, handleChangeRequestNavDrawer, handleOnSelect} = this.props;

        const style = {
            appBar: {
                position: 'fixed',
                top: 0,
                overflow: 'hidden',
                maxHeight: 57
            },
            menuButton: {
                marginLeft: 10
            },
            iconsRightContainer: {
                marginLeft: 20
            }
        };

        return (
            <div>
                <AppBar
                    style={{...styles, ...style.appBar}}
                    title={
                        <SearchBox data={this.props.data} onSelect={handleOnSelect}/>
                    }
                    iconElementLeft={
                        <IconButton style={style.menuButton} onClick={handleChangeRequestNavDrawer}>
                            <Menu color={white} />
                        </IconButton>
                    }

                />
            </div>
        );
    }
}

Header.propTypes = {
    styles: PropTypes.object,
    handleChangeRequestNavDrawer: PropTypes.func,
    handleOnSelect: PropTypes.func
};

export default Header;
