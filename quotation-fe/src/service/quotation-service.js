import axios from "axios";
import jwt_decode from "jwt-decode";

// url base
axios.defaults.baseURL = "https://quotation-system-be.herokuapp.com";

// getToken
const getToken = () => {
  let token = localStorage.getItem("token_access");
  return token;
};
const getUser = () => {
  return jwt_decode(getToken()).user_id.toString();
};

// get list of quotations
const getQuotationsList = () =>
  axios
    .get(`/quotations/${getUser()}`, {
      headers: {
        Authorization: `Bearer ${getToken()}`,
      },
    })
    .then((response) => response.data.reverse());

// create quotation
const createQuotation = (quotation) =>
  axios
    .post(`/quotation/${getUser()}`, quotation, {
      headers: {
        Authorization: `Bearer ${getToken()}`,
      },
    })
    .then((response) => response.data);

// export functions
export const quotationServices = {
  getQuotationsList,
  createQuotation,
};
