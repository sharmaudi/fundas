import React from 'react';
import {Link} from "react-router-dom";
import {IconButton, IconMenu, MenuItem, ToolbarGroup, DropDownMenu} from "material-ui";
import {pink500, white} from "material-ui/styles/colors";
import ViewModule from 'material-ui/svg-icons/action/view-module';
import ArrowDropRight from 'material-ui/svg-icons/navigation-arrow-drop-right';
import {typography} from "material-ui/styles/index";
import Assessment from 'material-ui/svg-icons/action/assessment';


const styles = {
    toolbarActive: {
        fontWeight: typography.fontWeightMedium,
        fontSize: 20,
        color:'white'

    },
    menuItem: {
        fontWeight: typography.fontWeightMedium,
        fontSize: 20,
        color:'white',
        paddingTop:10

    },
    toolbarDropdown: {
        fontWeight: typography.fontWeightMedium,
        fontSize: 20,
        color:'white',
        margin:0,
        paddingLeft:0,
        paddingRight:0
    },
    toolbarInactive: {
        fontWeight: typography.fontWeightLight,
        fontSize:15,
        color:'white'
    },
    listStyle: {
        backgroundColor:'rgba(0,0,0,.9)'
    },
    underlineStyle: {
        backgroundColor:'white'
    }
};

export const CompanyMiddleToolbar = ({company, chartType, dataType}) => (
    (
        <ToolbarGroup lastChild={true}>


            <DropDownMenu
                style={styles.toolbarDropdown}
                underlineStyle={styles.underlineStyle}
                menuStyle={styles.toolbarDropdown}
                listStyle={styles.listStyle}
                value={chartType}
                labelStyle={styles.toolbarActive}
            >
                <MenuItem value={'analysis'}
                          primaryText="Analysis"
                          label="Charts"
                          style={chartType==='analysis'?(styles.toolbarActive):styles.toolbarInactive}

                          containerElement={<Link to={`/companies/${company}/analysis/${dataType}`}/>}
                />

                <MenuItem value={'performance'}
                          primaryText="Performance"
                          label="Charts"

                          style={chartType==='performance'?(styles.toolbarActive):styles.toolbarInactive}

                          containerElement={<Link
                              to={`/companies/${company}/performance/${dataType}`}/>}
                />
                <MenuItem value={'health'}
                          primaryText="Health"
                          label="Charts"

                          style={chartType==='health'?(styles.toolbarActive):styles.toolbarInactive}

                          containerElement={<Link
                              to={`/companies/${company}/health/${dataType}`}/>}
                />
                <MenuItem value={'valuation'}
                          primaryText="Valuation"
                          label="Charts"

                          style={chartType==='valuation'?(styles.toolbarActive):styles.toolbarInactive}

                          containerElement={<Link
                              to={`/companies/${company}/valuation/${dataType}`}/>}
                />
                <MenuItem value={'dividends'}
                          primaryText="Dividends"
                          label="Charts"

                          style={chartType==='dividends'?(styles.toolbarActive):styles.toolbarInactive}

                          containerElement={<Link
                              to={`/companies/${company}/dividends/${dataType}`}/>}
                />

                <MenuItem value={'momentum'}
                          primaryText="Momentum"
                          label="Charts"
                          style={chartType==='momentum'?(styles.toolbarActive):styles.toolbarInactive}

                          containerElement={<Link to={`/companies/${company}/momentum/${dataType}`}/>}
                />



            </DropDownMenu>

            <DropDownMenu
                style={styles.toolbarDropdown}
                underlineStyle={styles.underlineStyle}
                listStyle={styles.listStyle}

                value={dataType}
                labelStyle={styles.toolbarActive}
            >
            <MenuItem value={'standalone'}
                      style={dataType==='standalone'?(styles.toolbarActive):styles.toolbarInactive}
                      primaryText="Standalone"
                      label="Data Type"

                      containerElement={<Link
                          to={`/companies/${company}/${chartType}/standalone`}/>}
            />
            <MenuItem value={'consolidated'}
                      style={dataType==='consolidated'?(styles.toolbarActive):styles.toolbarInactive}
                      primaryText="Consolidated"
                      label="Data Type"

                      containerElement={<Link
                          to={`/companies/${company}/${chartType}/consolidated`}/>}
            />
            </DropDownMenu>


        </ToolbarGroup>
    )
);



export const CompanyIconToolbar = ({company, chartType, dataType}) => (
    (
        <IconMenu color={white}
                  iconButtonElement={
                      <IconButton><ViewModule color={white}/></IconButton>
                  }
                  targetOrigin={{horizontal: 'left', vertical: 'top'}}
                  anchorOrigin={{horizontal: 'left', vertical: 'top'}}
        >
            <MenuItem value={'analysis'}
                      primaryText="Analysis"
                      containerElement={<Link to={`/companies/${company}/analysis/${dataType}`}/>}
            />

            <MenuItem
                rightIcon={<ArrowDropRight/>}
                primaryText={'Charts'}
                menuItems={
                    (<div>
                            <MenuItem value={'performance'}
                                      primaryText="Performance"
                                      containerElement={<Link
                                          to={`/companies/${company}/performance/${dataType}`}/>}
                            />
                            <MenuItem value={'health'}
                                      primaryText="Health"
                                      containerElement={<Link
                                          to={`/companies/${company}/health/${dataType}`}/>}
                            />
                            <MenuItem value={'valuation'}
                                      primaryText="Valuation"
                                      containerElement={<Link
                                          to={`/companies/${company}/valuation/${dataType}`}/>}
                            />
                            <MenuItem value={'dividends'}
                                      primaryText="Dividends"
                                      containerElement={<Link
                                          to={`/companies/${company}/dividends/${dataType}`}/>}
                            />
                        </div>
                    )
                }

            />


            <MenuItem
                rightIcon={<ArrowDropRight/>}
                primaryText={'Data Type'}
                menuItems={
                    (<div>
                            <MenuItem value={'standalone'}
                                      primaryText="Standalone"
                                      containerElement={<Link
                                          to={`/companies/${company}/${chartType}/standalone`}/>}
                            />
                            <MenuItem value={'consolidated'}
                                      primaryText="Consolidated"
                                      containerElement={<Link
                                          to={`/companies/${company}/${chartType}/consolidated`}/>}
                            />
                        </div>
                    )
                }

            />

        </IconMenu>
    )
);