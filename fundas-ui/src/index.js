import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import React from 'react';
import {store, history} from './store';
import './styles.scss';
import 'font-awesome/css/font-awesome.css';
import 'flexboxgrid/css/flexboxgrid.css';


import { Route, Switch } from 'react-router-dom';
import {ConnectedRouter} from 'react-router-redux'
import registerServiceWorker from './registerServiceWorker';
import App from './components/App';

ReactDOM.render((
    <Provider store={store}>
        <ConnectedRouter history={history}>
            <Switch>
                <Route path="/" component={App} />
            </Switch>
        </ConnectedRouter>
    </Provider>

), document.getElementById('root'));
registerServiceWorker();
