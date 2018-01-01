import {
    APP_LOAD,
    REDIRECT,
    HOME_PAGE_UNLOADED, ASYNC_START, ASYNC_END
} from '../constants/actionTypes';

const defaultState = {
    appName: 'Fundas',
    token: null,
    viewChangeCounter: 0,
    error: false
};

export default (state = defaultState, action) => {
    switch (action.type) {
        case APP_LOAD:
            if (action.error) {
                return {
                    ...state,
                    error: true,
                    appLoaded: false
                }
            }

            return {
                ...state,
                companies: action.payload.companies || null,
                appLoaded: true
            };



        case ASYNC_START:
            return {
                ...state,
                asyncPending:true
            };
        case ASYNC_END:
            return {
                ...state,
                asyncPending:false
            };
        case REDIRECT:
            return {...state, redirectTo: null};

        case HOME_PAGE_UNLOADED:
        default:
            return state;
    }
};
