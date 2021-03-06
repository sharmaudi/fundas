import React from 'react';
import Drawer from 'material-ui/Drawer';
import {spacing, typography} from 'material-ui/styles';
import {blue600, white} from 'material-ui/styles/colors';
import MenuItem from 'material-ui/MenuItem';
import {Link} from 'react-router-dom';
import Avatar from 'material-ui/Avatar';
import PropTypes from 'prop-types'
import ArrowDropRight from 'material-ui/svg-icons/navigation-arrow-drop-right';
import avatar from '../images/avatar.jpg'

const LeftDrawer = (props) => {
    let { navDrawerOpen } = props;

    const styles = {
        logo: {
            cursor: 'pointer',
            fontSize: 22,
            color: typography.textFullWhite,
            lineHeight: `${spacing.desktopKeylineIncrement}px`,
            fontWeight: typography.fontWeightLight,
            backgroundColor: blue600,
            paddingLeft: 40,
            height: 56,
        },
        menuItem: {
            color: white,
            fontSize: 14
        },
        avatar: {
            div: {
                padding: '15px 0 20px 15px',
                backgroundImage:  'url(' + require('../images/material_bg.png') + ')',
                maxHeight:80
            },
            icon: {
                float: 'left',
                display: 'block',
                marginRight: 15,
                boxShadow: '0px 0px 0px 8px rgba(0,0,0,0.2)'
            },
            span: {
                paddingTop: 12,
                display: 'block',
                color: 'white',
                fontWeight: 300,
                textShadow: '1px 1px #444'
            }
        }
    };

    return (
        <Drawer
            docked={true}
            open={navDrawerOpen}>
            <div style={styles.logo}>
                Fundas!
            </div>
            <div style={styles.avatar.div}>
                <Avatar src={avatar}
                        size={50}
                        style={styles.avatar.icon}/>
                <span style={styles.avatar.span}>{props.username}</span>
            </div>
            <div>
                {props.menus.map((menu, index) =>
                {

                    let disabled = false
                    if (menu.disabled && !props.company){
                        disabled = true;
                        return null;
                    }

                    if(menu.items) {
                        return <MenuItem
                            key={index}
                            style={styles.menuItem}
                            disabled={disabled}
                            rightIcon={<ArrowDropRight />}
                            primaryText={menu.text}
                            leftIcon={menu.icon}
                            menuItems={menu.items.map((subMenu,index) => (
                                <MenuItem
                                    key={index}
                                    primaryText={subMenu.text}
                                    containerElement={<Link to={`/companies/${props.company}/${subMenu.link}`}/>}
                                />
                            ))}
                            containerElement={<Link to={menu.link}/>}
                        />
                    }
                 return (
                     <MenuItem
                        key={index}
                        style={styles.menuItem}
                        primaryText={menu.text}
                        leftIcon={menu.icon}
                        containerElement={<Link to={menu.isRelative?`/companies/${props.company}/${menu.link}`:menu.link}/>}
                    />
                 )
                }
                )}
            </div>


        </Drawer>
    );
};

LeftDrawer.propTypes = {
    navDrawerOpen: PropTypes.bool,
    menus: PropTypes.array,
    username: PropTypes.string,
    company: PropTypes.string
};

export default LeftDrawer;
