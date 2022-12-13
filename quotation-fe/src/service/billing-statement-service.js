import axios from "axios";
import jwt_decode from "jwt-decode";

// url base
axios.defaults.baseURL = "http://127.0.0.1:8000";

// getToken
const getToken = () => {
  let token = localStorage.getItem("token_access");
  return token;
};
const getUser = () => {
  return jwt_decode(getToken()).user_id.toString();
};

// get list of cuentas de cobro
const getBillingStatementsList = () =>
  axios
    .get(`/billingStatement/${getUser()}`, {
      headers: {
        Authorization: `Bearer ${getToken()}`,
      },
    })
    .then((response) => response.data);

// get list of of cuentas de cobro
const getBillingStatementDetail = (billingStatementId) =>
  axios
    .get(`/billingStatement/${getUser()}/${billingStatementId}`, {
      headers: {
        Authorization: `Bearer ${getToken()}`,
      },
    })
    .then((response) => response.data);

// create  cuentas de cobro
const createBillingStatement = (quotationId) =>
  axios
    .post(`/billingStatement/${getUser()}`, quotationId, {
      headers: {
        Authorization: `Bearer ${getToken()}`,
      },
    })
    .then((response) => response.data);

// export functions
export const billingStatementServices = {
  getBillingStatementsList,
  createBillingStatement,
  getBillingStatementDetail,
};
