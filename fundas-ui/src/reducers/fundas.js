import {
    COMPANY_LOAD,
    FUNDAS_PAGE_LOADED,
    FUNDAS_PAGE_UNLOADED,
    CHANGE_DATA_TYPE, FEATURED_LOAD, MOMENTUM_LOAD, PORTFOLIO_LOAD
} from '../constants/actionTypes';

const defaultState = {
  dataType: 'standalone'
};

export default (state = defaultState, action) => {
    switch (action.type) {
        case FUNDAS_PAGE_LOADED:
            return {
                ...state,
                company: action.payload[0].company
            };


        case FUNDAS_PAGE_UNLOADED:
            return {};

        case COMPANY_LOAD:
            if (action.error) {
                return {
                    ...state,
                    error: true,
                    errorMsg: action.errorMsg
                };
            }

            return {
                ...state,
                company: action.company,
                companyDataSet: action.payload
            };

        case CHANGE_DATA_TYPE:
            return {
                ...state,
                dataType:action.payload.dataType
            };

        case FEATURED_LOAD:
            return {
                ...state,
                featured:action.payload
            };
        case PORTFOLIO_LOAD:
            return {
                ...state,
                portfolio:action.payload
            };
        case MOMENTUM_LOAD:
            return {
                ...state,
                momentum:action.payload
            };

        default:
            return state;
    }
}