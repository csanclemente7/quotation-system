<template>
  <div class="quotation">
    <div class="quotation-data">
      <h1 class="quotation__subtitle">
        <img src="../assets/img/quotation_img.png" alt="" />&nbsp; Nueva
        Cotización
      </h1>
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
      error_createQuotation: false,
      error_updateQuotation: false,
      showAll: false,
      index: 0,
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
.quotation {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: absolute;
  width: 100%;
  z-index: 2;
}

.quotation-data {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  width: 90%;
}
.quotation-data img {
  margin-top: 20px;
  width: 80px;
  margin-bottom: 5%;
}

.quotation__subtitle {
  display: flex;
  justify-content: center;
  align-items: center;
}

.quotation h1 {
  font-size: 50px;
  color: var(--text);
}

@media screen and (max-width: 768px) {
  .quotation-data h1 {
    font-size: 30px;
  }
  .quotation-data img {
    width: 50px;
  }
}

@import "../assets/css/common/filters.css";
@import "../assets/css/common/inputs.css";
@import "../assets/css/common/button.css";
@import "../assets/css/common/checkbox.css";
@import "../assets/css/common/links.css";
@import "../assets/css/base/base.css";
</style>