import React, {Component} from 'react';
import {connect} from "react-redux";
import withWidth from "material-ui/utils/withWidth";
import compose from "recompose/compose";
import {PORTFOLIO_LOAD} from "../../constants/actionTypes";
import {Paper} from "material-ui";
import agent, {tasks} from "../../agent";
import TaskWidget from "./TaskWidget";
import Assessment from 'material-ui/svg-icons/action/assessment';


class DashboardPage extends Component {

    state = {
        watchlist_task_id: null,
        portfolio_task_id: null,
        bhavcopy_task_id: null,
        watchlist_interval: null,
        portfolio_interval: null,
        bhavcopy_interval: null,
        w_t_p:null,
        p_t_p:null,
        b_t_p:null
    };

    componentWillMount() {
        if (!this.props.portfolio) {
            this.props.loadPortfolio(agent.companies.getPortfolio())
        }
    }

    analysePortfolio() {
        console.log("Analysing portfolio");
        tasks.analysePortfolio().then(res => {
            console.log(`Response: `, res);
            this.setState({
                portfolio_task_id: res.task_id
            });
            this.setState({
                portfolio_interval: setInterval(() => {
                    console.log(`Checking progress for ${res.task_id}`);
                    tasks.taskStatus('analyse_portfolio', res.task_id).then(r => {
                        this.setState({
                            p_t_p: r
                        });
                        console.log("Progress: ", r);
                        if(r.status === "done") {
                            clearInterval(this.state.portfolio_interval);
                            this.setState({
                                portfolio_task_id: null,
                                portfolio_interval: null,
                            })
                        }
                    })
                }, 3000)
            })
        })
    }

    analyseWatchlist() {
        console.log("Analysing watchlist")
        tasks.analyseWatchlist().then(res => {
            console.log(`Response: `, res)
            this.setState({
                watchlist_task_id: res.task_id
            })
            this.setState({
                watchlist_interval: setInterval(() => {
                    console.log(`Checking progress for ${res.task_id}`)
                }, 3000)
            })
        })
    }

    downloadBhavcopy() {
        console.log("Downloading bhavcopy")
        tasks.downloadBhavcopy().then(res => {
            console.log(`Response: `, res)
            this.setState({
                bhavcopy_task_id: res.task_id
            });
            this.setState({
                bhavcopy_interval: setInterval(() => {
                    console.log(`Checking progress for ${res.task_id}`)
                }, 3000)
            })

        })
    }

    componentWillUnmount() {
        console.log("Clearing intervals");
        clearInterval(this.state.bhavcopy_interval)
        clearInterval(this.state.watchlist_interval)
        clearInterval(this.state.portfolio_interval)

    }

    render() {
        return (
            <Paper className="row">

                <div className="col-xs-12 col-sm-12 col-md-6 col-lg-4">
                    <TaskWidget
                        title={"Watchlist"}
                        label={"Analyse Watchlist"}
                        onclick={tasks.analyseWatchlist}
                        args={[]}
                        taskType={"analyse_watchlist"}
                        Icon={Assessment}
                        goto={'/featured/standalone'}

                    />
                </div>

                <div className="col-xs-12 col-sm-12 col-md-6 col-lg-4">

                <TaskWidget
                    title={"Portfolio"}
                    label={"Analyse Portfolio"}
                    onclick={tasks.analysePortfolio}
                    args={[]}
                    taskType={"analyse_portfolio"}
                    Icon={Assessment}
                    goto={'/portfolio/performance'}


                />
                </div>

                <div className="col-xs-12 col-sm-12 col-md-6 col-lg-4">

                <TaskWidget
                    title={"Bhavcopy"}
                    label={"Download Bhavcopy"}
                    onclick={tasks.downloadBhavcopy}
                    args={['Periods']}
                    taskType={"download_bhavcopy"}
                    Icon={Assessment}
                    goto={'/featured/standalone'}



                />
                </div>


            </Paper>
        );
    }
}

DashboardPage.propTypes = {};
DashboardPage.defaultProps = {};

const mapStateToProps = state => {
    return {
        portfolio: state.fundas.portfolio
    }
};


const mapDispatchToProps = dispatch => ({
    loadPortfolio: (payload) => dispatch({
        type: PORTFOLIO_LOAD,
        payload,
        skipTracking: false
    })
});
export default compose(withWidth(), connect(mapStateToProps, mapDispatchToProps))(DashboardPage);