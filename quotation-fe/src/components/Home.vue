<template>
  <div class="home">
    <div class="home-data">
      <h1 class="home__subtitle">
        <img src="../assets/img/home_img.png" alt="" />&nbsp; App Cotizaciones
      </h1>
      <div class="input-container">
        <button v-on:click="openPopUp('quotation')" class="button">
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

  <!-- POPUPS -->
  <section class="popups_container">
    <!--- pop up create quotation -->
    <div class="popup" v-if="popUps.quotation">
      <div class="popup-close-container">
        <div class="popup_close" v-on:click="closePopUp('quotation')">
          <svg
            width="25"
            height="25"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            stroke="red"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="1.5"
            viewBox="0 0 24 24"
          >
            <path
              d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"
            />
          </svg>
        </div>
      </div>

      <div class="create-report__errors">
        <i
          class="fa fa-exclamation-circle"
          id="error-icon"
          v-if="errors.error_message"
        ></i>
        <span v-if="!errors.error_createQuotation" class="text_success">{{
          " " + success_message
        }}</span>
        <span v-if="errors.error_createQuotation" class="text_fail">{{
          " " + errors.error_message
        }}</span>
      </div>

      <h1 class="popup_title">
        <img src="../assets/img/quotation_img.png" alt="" />&nbsp; Nueva
        Cotización
      </h1>

      <!--- Placa -->
      <div class="header-form">
        <div class="input-container">
          <input
            type="text"
            name="cliente"
            id="placa"
            class="input cliente"
            v-model="quotation.cliente"
            maxlength="7"
          />
          <label class="input-label" for="cliente">Cliente</label>
          <span class="input-message-error">Este campo no es valido</span>
        </div>
      </div>

      <!--- FORM -->
      <form
        v-on:submit.prevent="createQuotationItem"
        class="formulario flex flex--column"
        id="form-quotation"
      >
        <!-- <button class="button" type="submit">Generar</button> -->

        <div
          class="row-form"
          v-for="(itemQuotation, index) in itemsQuotation"
          :key="index"
        >
          <div class="input-container item">
            <input
              type="text"
              name="item"
              id="item"
              class="input"
              v-model="itemQuotation.item"
            />
            <label class="input-label" for="item">Item</label>
            <span class="input-message-error">Este campo no es valido</span>
          </div>
          <div class="input-container price">
            <input
              type="text"
              name="price"
              id="price"
              class="input"
              v-model="itemQuotation.price"
            />
            <label class="input-label" for="price">Precio</label>
            <span class="input-message-error">Este campo no es valido</span>
          </div>

          <div class="input-container quantity">
            <input
              type="text"
              name="quantity"
              id="quantity"
              class="input"
              v-model="itemQuotation.quantity"
            />
            <label class="input-label" for="quantity">Cantidad</label>
            <span class="input-message-error">Este campo no es valido</span>
          </div>

          <div class="input-container total">
            <input
              type="text"
              name="total"
              id="total"
              class="input"
              v-model="itemQuotation.total"
            />
            <label class="input-label" for="total">Total</label>
            <span class="input-message-error">Este campo no es valido</span>
          </div>
        </div>

        <!-- BOTON AGREGAR ITEM -->
        <button
          class="button add-item"
          v-on:click="createItemQuotation"
          type="button"
        >
          <i class="fas fa-plus"></i>
        </button>

        <div class="input-container">
          <button class="button" type="submit">Generar</button>
        </div>
      </form>
    </div>
  </section>
</template>
<script>
import axios from "axios";
import jwt_decode from "jwt-decode";
import { itemServices } from "../service/item-service";
import { quotationServices } from "../service/quotation-service";

export default {
  name: "Home",
  data: function () {
    return {
      email: localStorage.getItem("email") || "none",
      is_admin: false,
      name: "",
      startLoader: false,
      tableRow: "",
      success_message: "",
      counter: 0,
      form: null,

      errors: {
        error_createQuotation: false,
        error_message: "",
      },

      popUps: {
        quotation: false,
      },

      quotation: {
        client: "",
        iva: "19",
        discount: "",
        subtotal: "",
        totalDiscount: "",
        totalIva: "",
        total: "",
      },

      items: [],

      quotations: [],

      itemsQuotation: [],
    };
  },

  mounted() {
    this.form = document.getElementById("form-quotation");
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

    // pop ups
    openPopUp: function (popUp, reporte) {
      this.popUps[popUp] = true;
    },
    closePopUp: function (popUp) {
      this.popUps[popUp] = false;
    },

    createItemQuotation: function () {
      let itemQuotation = {
        quotation: "",
        item: "",
        price: "",
        quantity: "",
        total: "",
      };
      this.itemsQuotation.push(itemQuotation);
    },
  },

  created: function () {
    this.verifyAuth();
    this.name = localStorage.getItem("name") || "";
    this.is_admin = JSON.parse(localStorage.getItem("isAdmin")) || false;
    this.createItemQuotation();

    itemServices.getItemsList().then((result) => {
      this.items = result;
    });

    quotationServices.getQuotationsList().then((result) => {
      this.quotations = result;
    });
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

.home__subtitle {
  display: flex;
  justify-content: center;
  align-items: center;
}

.home h1 {
  font-size: 50px;
  color: var(--text);
}

@media screen and (max-width: 768px) {
  .home-data h1 {
    font-size: 30px;
  }
  .home-data img {
    width: 80px;
  }
}
@import "../assets/css/common/popUp.css";
@import "../assets/css/common/inputs.css";
@import "../assets/css/common/button.css";
@import "../assets/css/base/base.css";
</style>