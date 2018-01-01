import superagentPromise from 'superagent-promise'
import _superagent from 'superagent'

const superagent = superagentPromise(_superagent, global.Promise);

//const encode = encodeURIComponent;
const responseBody = res => res.body;


const API_ROOT = 'http://192.168.2.100:8000/api/v1';

const requests = {
    del: url =>
        superagent.del(`${API_ROOT}${url}`).then(responseBody),
    get: url =>
        superagent.get(`${API_ROOT}${url}`).then(responseBody),
    put: (url, body) =>
        superagent.put(`${API_ROOT}${url}`, body).then(responseBody),
    post: (url, body) =>
        superagent.post(`${API_ROOT}${url}`, body).then(responseBody)
};

const companies = {
    all: () => requests.get(`/companies/`),
    getCompany: (symbol) => requests.get(`/companies/${symbol}`),
    getFeatured: () => requests.get(`/featured/`),
    getMomentum: (symbol) => requests.get(`/companies/${symbol}/momentum/`)
};

export default {
    companies
}