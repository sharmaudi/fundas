import { combineReducers } from 'redux';
import home from './reducers/home';
import fundas from './reducers/fundas';
import common from './reducers/common'
import { routerReducer } from 'react-router-redux';

export default combineReducers({
    home,
    fundas,
    common,
    router: routerReducer
});
