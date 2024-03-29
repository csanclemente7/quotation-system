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

// get list of quotations
const getQuotationsList = () =>
  axios
    .get(`/quotations/${getUser()}`, {
      headers: {
        Authorization: `Bearer ${getToken()}`,
      },
    })
    .then((response) => {
      localStorage.setItem("quotations", JSON.stringify(response.data));
      return response.data.sort((a, b) => b.id - a.id);
    });

// create quotation
const createQuotation = (quotation) =>
  axios
    .post(`/quotation/${getUser()}`, quotation, {
      headers: {
        Authorization: `Bearer ${getToken()}`,
      },
    })
    .then((response) => response.data);

// update quotation
const updateQuotation = (quotation) =>
  axios
    .put(`/quotation/${getUser()}/${quotation.id}/update`, quotation, {
      headers: {
        Authorization: `Bearer ${getToken()}`,
      },
    })
    .then((response) => response.data);

const deleteQuotation = (quotationId) =>
  axios
    .delete(`/quotation/${getUser()}/${quotationId}/delete`, {
      headers: {
        Authorization: `Bearer ${getToken()}`,
      },
    })
    .then((response) => response.data);

// export functions
export const quotationServices = {
  getQuotationsList,
  createQuotation,
  updateQuotation,
  deleteQuotation,
};
