import React, {Component} from 'react';
import PropTypes from 'prop-types';
import globalStyles from "../../styles";
import {IconButton, IconMenu, MenuItem, Paper} from "material-ui";
import {typography} from "material-ui/styles/index";
import {cyan600, white} from "material-ui/styles/colors";
import InfoWidget from "./InfoWidget";
import {Link} from "react-router-dom";
import ReactPaginate from 'react-paginate';
import MoreVertIcon from 'material-ui/svg-icons/navigation/more-vert';
import ContentFilter from 'material-ui/svg-icons/content/filter-list';
import Assessment from "material-ui/svg-icons/action/assessment"
import Info from "material-ui/svg-icons/action/info"
import Timeline from "material-ui/svg-icons/action/timeline"


class InfoView extends Component {

    constructor(props) {
        super(props);
        this.state = {
            data: [],
            offset: 0,
            tabIndex: props.slideIndex,
            dataType: props.dataType
        }
    }

    getData(dataType) {
        const limit = this.props.perPage;
        const offset = this.state.offset;

        const {featured} = this.props;
        dataType = dataType || this.state.dataType;
        let company_list = dataType==='standalone'?featured.sort_order_standalone:featured.sort_order_consolidated;
        const data = company_list.slice(offset, offset + limit);

        console.log("Company list", company_list);
        console.log("Data", data);
        this.setState({
            data: data,
            pageCount: Math.ceil(company_list.length / this.props.perPage)
        });

        console.log("State is ", this.state)

    }

    componentDidMount() {
        this.getData()
    }

    componentWillUpdate(nextProps, nextState) {
        if(this.state.dataType !== nextState.dataType) {
            this.getData(nextState.dataType);
        }
    }


    handlePageClick = (data) => {
        console.log("Handing click", data);
        let selected = data.selected;
        let offset = Math.ceil(selected * this.props.perPage);
        this.setState({offset: offset}, () => {
            this.getData();
        });
    };

    handleMenuItemClick = (event, value) => {
        this.setState({
            tabIndex:value
        })
    };

    handleDataItemClick = (event, value) => {
        this.setState({
            dataType:value
        });
        this.getData()
    };



    render() {
        const style ={
            paper: {
                minHeight: 200,
                minWidth: 200,
                height:300,
                width:300,
                margin: 10,
                textAlign: 'center',
            },
            title: {
                padding:10,
                fontSize: 24,
                fontWeight: typography.fontWeightLight,
                backgroundColor: cyan600,
                textDecoration:'none',
                color: white
            },
            titleText: {
                fontSize: 24,
                fontWeight: typography.fontWeightLight,
                textDecoration:'none',
                color: white
            },

            titleLink: {
                textDecoration:'none',
            },
            progress: {
                padding: 20
            }



        };
        const featured = this.props.featured;
        const dataType = this.props.dataType || 'standalone';
        let c_data = this.state.data;


        console.log(`Slide Index ${this.props.slideIndex}`);

        return (
            <div>
                <div className="row">

                    <div className="col-lg-6">
                        <IconMenu
                            iconButtonElement={<IconButton><MoreVertIcon /></IconButton>}
                            anchorOrigin={{horizontal: 'left', vertical: 'top'}}
                            targetOrigin={{horizontal: 'left', vertical: 'top'}}
                            onChange={this.handleMenuItemClick.bind(this)}
                            value={this.state.tabIndex}
                        >
                            <MenuItem
                                primaryText="Info"
                                value={0}
                                leftIcon={<Info />}
                            />

                            <MenuItem
                                primaryText="Analysis"
                                value={1}
                                leftIcon={<Assessment />}
                            />

                            <MenuItem
                                primaryText="Performance"
                                value={2}

                                leftIcon={<Timeline />}
                            />


                        </IconMenu>
                        <IconMenu
                            iconButtonElement={<IconButton><ContentFilter /></IconButton>}
                            anchorOrigin={{horizontal: 'left', vertical: 'top'}}
                            targetOrigin={{horizontal: 'left', vertical: 'top'}}
                            onChange={this.handleDataItemClick.bind(this)}
                            value={this.state.dataType}
                        >
                            <MenuItem
                                primaryText="Standalone"
                                value="standalone"
                            />

                            <MenuItem
                                primaryText="Consolidated"
                                value="consolidated"
                            />



                        </IconMenu>
                    </div>

                    <div className="col-lg-4 col-lg-offset-1 text-right" >
                        <ReactPaginate previousLabel={"previous"}
                                       nextLabel={"next"}
                                       breakLabel={<a href="">...</a>}
                                       breakClassName={"break-me"}
                                       pageCount={this.state.pageCount}
                                       marginPagesDisplayed={2}
                                       pageRangeDisplayed={5}
                                       onPageChange={this.handlePageClick}
                                       containerClassName={"pagination"}
                                       subContainerClassName={"pages pagination"}
                                       activeClassName={"active"} />
                    </div>
                </div>
                <div style={globalStyles.section} className="row">


                    {c_data.map(company => {

                        return (
                            <div key={company} className="col-xs-12 col-sm-6 col-md-6 col-lg-4 col-md m-b-15">
                                <Paper style={style.paper} zDepth={3}>
                                    <div style={style.title}><Link style={style.titleLink} to={`/companies/${company}/${dataType}`}>
                                        <span style={style.titleText}>
                                           {company}
                                        </span>
                                        </Link>
                                    </div>
                                    <InfoWidget
                                        featured={featured}
                                        height={style.paper.height}
                                        width={style.paper.width}
                                        dataType={this.state.dataType}
                                        company={company}
                                        slideIndex={this.state.tabIndex}
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

InfoView.propTypes = {
    featured:PropTypes.object,
    dataType:PropTypes.string,
    slideIndex:PropTypes.number,
    perPage:PropTypes.number
};
InfoView.defaultProps = {
    perPage: 12,
    slideIndex: 1
};

export default InfoView;
