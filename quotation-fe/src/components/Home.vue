<template>
  <div class="home">
    <div class="home-data">
      <h1 class="login__subtitle">
        <img src="../assets/img/home_img.png" alt="" />&nbsp; Quotation App
      </h1>
      <div class="input-group-home">
        <button v-on:click="loadQuotation()" class="btn-home-1">
          Nueva Cotización
        </button>
      </div>
    </div>
  </div>
  <!-- LOADER -->
  <div class="lds-spinner" v-if="startLoader">
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
  </div>
</template>
<script>
import axios from "axios";
import jwt_decode from "jwt-decode";
import swal from "sweetalert";
export default {
  name: "Home",
  data: function () {
    return {
      email: localStorage.getItem("email") || "none",
      is_admin: false,
      name: "",
      startLoader: false,
      error_message: "",
      success_message: "",
      error_createReport: false,
      error_updateReport: false,
      showAll: false,
      index: 0,
      tableRow: "",
    };
  },

  methods: {
    // database methods

    verifyAuth: function () {
      this.is_auth = localStorage.getItem("isAuth") || false;
      if (this.is_auth == false) {
        this.$router.push("logIn");
      }
    },

    // other methods

    loadQuotation: function () {
      this.$router.push("quotation");
    },
    verifyToken: function () {
      this.startLoader = true;
      return axios
        .post(
          "https://quotation-system-be.herokuapp.com/refresh",
          { refresh: localStorage.getItem("token_refresh") },
          { headers: {} }
        )
        .then((result) => {
          localStorage.setItem("token_access", result.data.access);
          this.startLoader = false;
        })
        .catch(() => {
          this.$emit("logOut");
        });
    },
  },

  created: function () {
    this.verifyAuth();
    this.name = localStorage.getItem("name") || "";
    this.is_admin = JSON.parse(localStorage.getItem("isAdmin")) || false;
  },
};
</script>
<style>
.home {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: absolute;
  width: 100%;
  z-index: 2;
}

.home-data {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  width: 90%;
}
.home-data img {
  margin-top: 20px;
  width: 150px;
  margin-bottom: 5%;
}

.login__subtitle {
  display: flex;
  justify-content: center;
  align-items: center;
}

.home-data .data-item {
  margin-bottom: 5%;
}

.home-data .home__text {
  color: var(--text-light);
}

.home h1 {
  font-size: 50px;
  color: var(--text);
}
.home h2 {
  font-size: 50px;
  color: var(--text-light-dark);
}
.home span {
  color: crimson;
  font-weight: bold;
}

.input-group-home {
  width: 100%;
  margin: 0 auto;
  margin-bottom: 1.5rem;
}

.input-group-home button {
  border: 1px solid var(--text);
  border-radius: 5px;
  padding: 0.7rem 0;
  width: 30%;
  line-height: 1.6rem;
  font-size: 1.3rem;
  transition: 0.3s ease-in-out all;
  font-weight: 500;
}

.btn-home-1 {
  background-color: var(--color-secondary);
  color: #ffffff;
}

.btn-home-1:hover {
  cursor: pointer;
  background-color: var(--color-secondary-dark);
}

.btn-home-2 {
  background-color: #262626;
  color: #ffffff;
}

.btn-home-2:hover {
  cursor: pointer;
  background-color: var(--color-secondary-dark);
}

@media screen and (max-width: 768px) {
  .btn-home-2 {
    width: 100%;
  }
  .btn-home-1 {
    width: 100%;
  }
  .home-data h1 {
    font-size: 30px;
  }
  .home-data h2 {
    font-size: 25px;
  }
  .home-data img {
    width: 100px;
  }

  .input-group-home button {
    width: 80%;
    padding: 0.5rem 0;
  }
}

@import "../assets/css/componentes/filters.css";
@import "../assets/css/componentes/inputs.css";
@import "../assets/css/componentes/button.css";
@import "../assets/css/componentes/checkbox.css";
@import "../assets/css/componentes/links.css";
@import "../assets/css/componentes/table.css";
@import "../assets/css/componentes/tableMobile.css";
/* @import "../assets/css/home/componentes/tableMobileResponsive.css"; */
@import "../assets/css/base/base.css";
</style>