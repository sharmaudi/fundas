import React, {Component} from 'react';
import PropTypes from 'prop-types';
import {tasks} from "../../agent";
import {FlatButton, LinearProgress, Paper, Snackbar, TextField} from "material-ui";
import {typography} from 'material-ui/styles';
import {cyan600, white} from 'material-ui/styles/colors';
import {push} from 'react-router-redux'
import {store} from '../../store';


class TaskWidget extends Component {

    state = {
        task_id: null,
        intv: null,
        taskProgress: null,
        snackbarOpen:false,
        message: null,
        param0Value: null,
        param1Value: null,
        param2Value: null,
    };

    handleRequestClose = () => {
        this.setState({
            snackbarOpen: false,
        });
    };

    handleActionClick = () => {
        this.setState({
            snackbarOpen: false,
        });
        store.dispatch(push(this.props.goto))
    };

    handleChangeParam0 = (event) => {
        this.setState({
            param0Value: event.target.value,
        });
    };

    performTask() {
        const {taskType, onclick, args, label} = this.props;
        const func = onclick;
        func(this.state.param0Value, this.state.param1Value, this.state.param2Value).then(res => {
            console.log(`Response: `, res);
            this.setState({
                task_id: res.task_id
            });
            this.setState({
                intv: setInterval(() => {
                    console.log(`Checking progress for ${res.task_id}`);
                    tasks.taskStatus(taskType, res.task_id).then(r => {
                        this.setState({
                            taskProgress: r
                        });
                        console.log("Progress: ", r);
                        if (r.status === "done") {
                            clearInterval(this.state.intv);
                            this.setState({
                                task_id: null,
                                intv: null,
                                snackbarOpen: true,
                                message: `${label} Completed`
                            })
                        }
                    })
                }, 3000)
            })
        })
    }


    render() {
        const style ={
            paper: {
                minHeight: 200,
                minWidth: 200,
                margin: 20,
                textAlign: 'center',
        },
            title: {
                fontSize: 24,
                fontWeight: typography.fontWeightLight,
                backgroundColor: cyan600,
                color: white
            },
            progress: {
                padding: 20
            }



        };

        return (


            <Paper style={style.paper} zDepth={3}>
                    <div style={style.title}>{this.props.title}</div>


                {this.props.args && this.props.args.map((arg, index) => (
                    <TextField
                        hintText={arg}
                        id="text-field-controlled"
                        value={this.state[`param${index}Value`]}
                        onChange={this.handleChangeParam0}
                    />
                ))}

                    <FlatButton
                        label={this.props.label}
                        onClick={this.performTask.bind(this)}
                        primary={true}/>
                    {this.state.task_id && (
                        <div style={style.progress}>
                            <LinearProgress mode="indeterminate"/>
                        </div>
                    )}

                {this.props.goto && (
                    <Snackbar
                        open={this.state.snackbarOpen}
                        message={this.state.message}
                        action="goto"
                        onActionClick={this.handleActionClick}
                        onRequestClose={this.handleRequestClose}
                    />
                )}

                {!this.props.goto && (
                    <Snackbar
                        open={this.state.snackbarOpen}
                        message={this.state.message}
                        onRequestClose={this.handleRequestClose}
                    />
                )}

            </Paper>

        );
    }

}

TaskWidget.propTypes = {
    title: PropTypes.string,
    label: PropTypes.string,
    onclick: PropTypes.func,
    taskType: PropTypes.string,
    args: PropTypes.array,
    className: PropTypes.string,
    Icon: PropTypes.any, // eslint-disable-line
    color: PropTypes.string

};
TaskWidget.defaultProps = {};

export default TaskWidget;
