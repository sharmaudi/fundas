import React, {Component} from 'react';
import EquityCurveChart from "./EquityCurveChart";
import compose from "recompose/compose";
import withWidth from "material-ui/utils/withWidth";
import {connect} from "react-redux";
import {Table, TableBody, TableHeader, TableHeaderColumn, TableRow, TableRowColumn,} from 'material-ui/Table';
import {Card, CardText, CardTitle} from "material-ui";

const  style = {
    stats: {
        color: '#4b1335',
        borderRadius:'5px',
        padding: '20px',
        fontSize: '120%'
    },
    statsContainer: {
        backgroundColor: '#fff',
        color: '#444',
    },
    statsHeading: {
        color: '#b97957',
        padding:10
    }
};

class PortfolioPerformance extends Component {
    render() {
        const portfolio = this.props.portfolio;


        if (!portfolio) {
            return (
                <div>Loading...</div>
            )
        }


        return (
            <div>


                <Card initiallyExpanded={true} style={{color:'grey'}}>
                    <CardTitle title={"Equity Curve"}
                               style={{backgroundColor:'lightgrey'}}
                               actAsExpander={true}
                               showExpandableButton={true}
                    >
                    </CardTitle>


                    <CardText expandable={true}>
                        <EquityCurveChart
                            portfolio={portfolio}/>
                    </CardText>

                </Card>


                <Card initiallyExpanded={true} style={{color:'grey'}}>
                    <CardTitle title={"Stats"}
                               style={{backgroundColor:'lightgrey'}}
                               actAsExpander={true}
                               showExpandableButton={true}
                    >
                    </CardTitle>


                    <CardText expandable={true}>
                        <Stats portfolio={portfolio}/>
                    </CardText>

                </Card>

                <Card initiallyExpanded={false} style={{color:'grey'}}>
                    <CardTitle title={"Open Positions"}
                               style={{backgroundColor:'lightgrey'}}
                               actAsExpander={true}
                               showExpandableButton={true}
                    >
                    </CardTitle>


                    <CardText expandable={true}>
                        <TableExampleSimple
                            portfolio={portfolio}
                        />
                    </CardText>

                </Card>


                <Card initiallyExpanded={false} style={{color:'grey'}}>
                    <CardTitle title={"Closed Positions"}
                               style={{backgroundColor:'lightgrey'}}
                               actAsExpander={true}
                               showExpandableButton={true}
                    >
                    </CardTitle>


                    <CardText expandable={true}>
                        <TableClosedPositions
                            portfolio={portfolio}
                        />
                    </CardText>

                </Card>




            </div>


        );
    }
}

const Stats = ({portfolio}) => (
  <div style={style.statsContainer} className='row'>
      <div style={style.stats} className='col-xs-12 col-sm-6 col-md-4 col-lg-4'>
          <span style={style.statsHeading}>Profit</span>{portfolio.performance.stats.totalProfit}
      </div>

      <div style={style.stats} className='col-xs-12 col-sm-6 col-md-4 col-lg-4'>
          <span style={style.statsHeading}>Open Profit</span> {portfolio.performance.stats.profit}
      </div>

      <div style={style.stats} className='col-xs-12 col-sm-6 col-md-4 col-lg-4'>
          <span style={style.statsHeading}>Closed Profit</span> {portfolio.performance.stats.closedProfit}
      </div>

      <div style={style.stats} className='col-xs-12 col-sm-6 col-md-4 col-lg-4'>
          <span style={style.statsHeading}>Profit %</span> {portfolio.performance.stats.profitPercentage}
      </div>

      <div style={style.stats} className='col-xs-12 col-sm-6 col-md-4 col-lg-4'>
          <span style={style.statsHeading}>CAGR</span> {portfolio.performance.stats.cagr}
      </div>

      <div style={style.stats} className='col-xs-12 col-sm-6 col-md-4 col-lg-4'>
          <span style={style.statsHeading}>Max Drawdown</span>  {portfolio.performance.stats.maxDrawdown}
      </div>

      <div style={style.stats} className='col-xs-12 col-sm-6 col-md-4 col-lg-4'>
          <span style={style.statsHeading}>Max Drawdown %</span> {portfolio.performance.stats.maxDrawdownPercentage}
      </div>

  </div>
);

const TableExampleSimple = ({portfolio}) => (
    <Table height={600}>
        <TableHeader displaySelectAll={false} adjustForCheckbox={false}>
            <TableRow>
                {
                    portfolio.performance.openPositions.columns.map(val => (
                        <TableHeaderColumn>{val.toUpperCase()}</TableHeaderColumn>
                    ))
                }
            </TableRow>
        </TableHeader>
        <TableBody stripedRows={true} displayRowCheckbox={false}>

            {
                portfolio.performance.openPositions.data.map(arr => (
                    <TableRow>{arr.map(val => (
                        <TableRowColumn>{val}</TableRowColumn>
                    ))}</TableRow>
                ))
            }
        </TableBody>
    </Table>
);

const TableClosedPositions = ({portfolio}) => (
    <Table height={600}>
        <TableHeader displaySelectAll={false} adjustForCheckbox={false}>
            <TableRow>
                {
                    portfolio.performance.closedPositions.columns.map(val => (
                        <TableHeaderColumn>{val.toUpperCase()}</TableHeaderColumn>
                    ))
                }
            </TableRow>
        </TableHeader>
        <TableBody
            stripedRows={true}
            displayRowCheckbox={false}>

            {
                portfolio.performance.closedPositions.data.map(arr => (
                    <TableRow>{arr.map(val => (
                        <TableRowColumn>{val}</TableRowColumn>
                    ))}</TableRow>
                ))
            }
        </TableBody>
    </Table>
);


PortfolioPerformance.propTypes = {};
PortfolioPerformance.defaultProps = {};

const mapStateToProps = state => {
    return {
        portfolio: state.fundas.portfolio
    }
};


const mapDispatchToProps = dispatch => ({});

export default compose(withWidth(), connect(mapStateToProps, mapDispatchToProps))(PortfolioPerformance);
