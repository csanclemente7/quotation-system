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

const createItemQuotation = (itemQuotation) =>
  axios
    .post(`/itemsQuotation/${getUser()}`, itemQuotation, {
      headers: {
        Authorization: `Bearer ${getToken()}`,
      },
    })
    .then((response) => response.data);

// export functions
export const itemQuotationServices = {
  createItemQuotation,
};
