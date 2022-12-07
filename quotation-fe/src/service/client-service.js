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

// get list of clients
const getClientsList = () =>
  axios
    .get(`/clients/${getUser()}`, {
      headers: {
        Authorization: `Bearer ${getToken()}`,
      },
    })
    .then((response) => response.data);

// create client
const createClient = (client) =>
  axios
    .post(`/client/${getUser()}`, client, {
      headers: {
        Authorization: `Bearer ${getToken()}`,
      },
    })
    .then((response) => response.data);

// export functions
export const clientServices = {
  getClientsList,
  createClient,
};
