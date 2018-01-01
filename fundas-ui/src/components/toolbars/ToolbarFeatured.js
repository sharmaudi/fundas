import React from 'react';
import {Link} from "react-router-dom";
import {IconButton, IconMenu, MenuItem, ToolbarGroup} from "material-ui";
import {white} from "material-ui/styles/colors";
import ViewModule from 'material-ui/svg-icons/action/view-module';
import {typography} from "material-ui/styles/index";


const styles = {
    toolbarActive: {
        fontWeight: typography.fontWeightMedium,
        fontSize: 20,
        color:'white'
    },
    toolbarInactive: {
        fontWeight: typography.fontWeightLight,
        color:'white'
    }
};

export const FeaturedRightToolbar = ({dataType}) => (
    (
        <ToolbarGroup
            firstChild={true}
            style={styles.toolbarItem}
        >

            <MenuItem value={'standalone'}
                      style={dataType === 'standalone' ? (styles.toolbarActive) : styles.toolbarInactive}
                      primaryText="Standalone"
                      containerElement={<Link
                          to={`/featured/standalone`}/>}
            />
            <MenuItem value={'consolidated'}
                      style={dataType === 'consolidated' ? (styles.toolbarActive) : styles.toolbarInactive}
                      primaryText="Consolidated"
                      containerElement={<Link
                          to={`/featured/consolidated`}/>}
            />


        </ToolbarGroup>
    )
);


export const FeaturedIconToolbar = ({dataType}) => (
    (
        <IconMenu color={white}
                  iconButtonElement={
                      <IconButton><ViewModule color={white}/></IconButton>
                  }
                  targetOrigin={{horizontal: 'left', vertical: 'top'}}
                  anchorOrigin={{horizontal: 'left', vertical: 'top'}}
        >
            <MenuItem value={'standalone'}
                      style={dataType === 'standalone' ? (styles.toolbarActive) : styles.toolbarInactive}
                      primaryText="Standalone"
                      containerElement={<Link
                          to={`/featured/standalone`}/>}
            />
            <MenuItem value={'consolidated'}
                      style={dataType === 'consolidated' ? (styles.toolbarActive) : styles.toolbarInactive}
                      primaryText="Consolidated"
                      containerElement={<Link
                          to={`/featured/consolidated`}/>}
            />

        </IconMenu>
    )
);