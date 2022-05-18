<template>
  <div class="home">
    <div class="home-data">
      <h1 class="home__subtitle">
        <img src="../assets/img/logo.png" alt="" />&nbsp; App Cotizaciones
      </h1>
      <div class="input-container">
        <button v-on:click="openPopUp('quotation')" class="button blue">
          Nueva Cotización
        </button>

        <div class="input-container">
          <button v-on:click="openPopUp('item')" class="button">Insumos</button>
        </div>
      </div>

      <!-- TABLE -->
      <table class="custom-responsiva">
        <thead>
          <tr>
            <th>#</th>
            <th>Fecha</th>
            <th>Cliente</th>
            <th>Valor</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="quotation in quotations"
            :key="quotation"
            id="table_row"
            v-on:click="openPopUp('updateReporte', reporte)"
          >
            <td>{{ quotation.id }}</td>
            <td>{{ quotation.date }}</td>
            <td>{{ quotation.client }}</td>
            <td>${{ priceToString(quotation.total) }}</td>
          </tr>
        </tbody>
      </table>
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

      <!--- FORM -->
      <form
        v-on:submit.prevent="processCreateQuotation"
        class="formulario flex flex--column"
        id="form-quotation"
      >
        <div class="header-form">
          <!--- Cliente -->
          <div class="input-container client">
            <input
              type="text"
              name="cliente"
              id="cliente"
              class="input"
              v-model="quotation.client_name"
              v-on:focus="openPopUpClientes(index)"
              autoComplete="off"
              required
            />
            <label class="input-label" for="cliente">Cliente</label>
            <button
              class="editbtn"
              type="button"
              aria-label="submit form"
              v-if="quotation.client_name != ''"
              v-on:click="editClientName"
            >
              <!-- edit icon -->
              <li class="fa fa-edit"></li>
            </button>
            <span class="input-message-error">Este campo no es valido</span>
          </div>
          <!--- Iva -->
          <div class="input-container iva">
            <input
              type="text"
              name="iva"
              id="iva"
              class="input"
              v-model="quotation.iva"
              maxlength="7"
              required
            />
            <label class="input-label" for="iva">% Iva</label>
            <span class="input-message-error">Este campo no es valido</span>
          </div>

          <!--- Descuento -->
          <div class="input-container descuento">
            <input
              type="text"
              name="descuento"
              id="descuento"
              class="input"
              v-model="quotation.discount"
              maxlength="7"
              required
            />
            <label class="input-label" for="descuento">% Descuento</label>
            <span class="input-message-error">Este campo no es valido</span>
          </div>
        </div>
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
              v-model="itemQuotation.name"
              v-on:focus="openPopUpSuggestions(index)"
              autocomplete="off"
              required
            />

            <label class="input-label" for="item">Item</label>
            <button
              class="editbtn"
              type="button"
              aria-label="submit form"
              v-if="itemQuotation.item != ''"
              v-on:click="editItemName"
            >
              <!-- edit icon -->
              <li class="fa fa-edit"></li>
            </button>

            <span class="input-message-error">Este campo no es valido</span>
          </div>
          <div class="input-container price">
            <input
              type="text"
              name="price"
              id="price"
              class="input"
              v-model="itemQuotation.price"
              v-on:focus="setIndexSuggestion(index)"
              v-on:input="setTotalItemQuotation"
              :disabled="itemQuotation.item === ''"
              autocomplete="off"
              required
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
              v-on:focus="setIndexSuggestion(index)"
              v-on:input="setTotalItemQuotation"
              :disabled="itemQuotation.price === ''"
              autocomplete="off"
              required
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
              autocomplete="off"
              required
              disabled
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

        <!-- totales -->
        <div class="table-results">
          <table class="table-totals custom-responsiva">
            <tbody>
              <tr>
                <td>Subtotal</td>
                <td>${{ priceToString(quotationResults.subtotal) }}</td>
              </tr>
              <tr>
                <td>Iva {{ quotation.iva }}%</td>
                <td>${{ priceToString(quotationResults.totalIva) }}</td>
              </tr>
              <tr v-if="quotation.discount > 0">
                <td>Descuento {{ quotation.discount }}%</td>
                <td>${{ priceToString(quotationResults.totalDiscount) }}</td>
              </tr>
              <tr>
                <td>Total</td>
                <td>${{ priceToString(quotationResults.total) }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="input-container">
          <button class="button" type="submit">Generar Cotización</button>
        </div>
      </form>
    </div>

    <!--- pop up create item -->
    <div class="popup" v-if="popUps.item">
      <div class="popup-close-container">
        <div class="popup_close" v-on:click="closePopUp('item')">
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
        <img src="../assets/img/quotation_img.png" alt="" />&nbsp; Agregar
        insumos
      </h1>

      <!--- Form -->
      <form class="item-create-form" v-on:submit.prevent="processCreateItem">
        <div class="header-form">
          <div class="input-container name">
            <input
              type="text"
              name="name"
              id="name"
              class="input"
              v-model="item.name"
              maxlength="70"
            />
            <label class="input-label" for="price">Item</label>
            <span class="input-message-error">Este campo no es valido</span>
          </div>
          <div class="input-container price">
            <input
              type="text"
              name="price"
              id="price"
              class="input"
              v-model="item.price"
              maxlength="30"
            />
            <label class="input-label" for="price">Precio</label>
            <span class="input-message-error">Este campo no es valido</span>
          </div>
          <div class="input-container">
            <button class="button" type="submit">Agregar</button>
          </div>
        </div>
      </form>

      <!-- TABLE -->
      <table class="custom-responsiva">
        <thead>
          <tr>
            <th>Item</th>
            <th>Precio</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="item in items"
            :key="item"
            id="table_row"
            v-on:click="openPopUp('updateReporte', reporte)"
          >
            <td>{{ item.name }}</td>
            <td>${{ priceToString(item.price) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <!--- finish pop up create item -->

    <!--- pop up suggestions -->
    <div class="popup popup-suggestions" v-if="popUps.suggestions">
      <div class="popup-close-container">
        <div class="popup_close" v-on:click="closePopUp('suggestions')">
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
      <div class="input-container suggestion-container">
        <input
          type="text"
          name="suggestion"
          id="suggestion"
          class="input"
          v-model="suggestion"
          v-on:focus="openPopUp('suggestions')"
          v-on:input="filterItems(suggestion)"
          autocomplete="off"
        />
        <label class="input-label" for="suggestion"> Buscar Item </label>
        <span class="input-message-error">Este campo no es valido</span>

        <div
          class="suggestion"
          v-for="(item, index) in suggestions"
          :key="index"
        >
          <li
            v-on:click="setItemSuggestion(item.id, item.name, item.price)"
            class="suggestion-item"
          >
            <div class="suggestion-content">
              <i class="fas fa-plus">&nbsp;</i>

              {{ item.name }}
              <p class="seggestion-price">
                &nbsp;&nbsp;$ {{ priceToString(item.price) }}
              </p>
            </div>
          </li>
        </div>
      </div>
    </div>

    <!--- pop up clientes -->
    <div class="popup popup-clientes" v-if="popUps.clientes">
      <div class="popup-close-container">
        <div class="popup_close" v-on:click="closePopUp('clientes')">
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
      <div class="input-container suggestion-container">
        <input
          type="text"
          name="suggestion"
          id="suggestion"
          class="input"
          v-model="suggestion"
          v-on:focus="openPopUp('clientes')"
          v-on:input="filterClients(suggestion)"
          autocomplete="off"
        />
        <label class="input-label" for="suggestion"> Buscar Cliente </label>
        <span class="input-message-error">Este campo no es valido</span>

        <div
          class="suggestion"
          v-for="(client, index) in suggestions"
          :key="index"
        >
          <li
            v-on:click="
              setClientSuggestion(client.id, client.name, client.phone)
            "
            class="suggestion-item"
          >
            <div class="suggestion-content">
              <i class="fas fa-plus">&nbsp;</i>

              {{ client.name }}
              <p class="seggestion-price">
                &nbsp;&nbsp;Tel: {{ client.phone }}
              </p>
            </div>
          </li>
        </div>
      </div>
    </div>
  </section>
</template>
<script>
import axios from "axios";
import jwt_decode from "jwt-decode";
import { itemServices } from "../service/item-service";
import { quotationServices } from "../service/quotation-service";
import { clientServices } from "../service/client-service";
import { itemQuotationServices } from "../service/item-quotation-service";

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
      suggestions: "",
      indexSuggestion: 0,

      errors: {
        error_createQuotation: false,
        error_message: "",
      },

      popUps: {
        clientes: false,
        quotation: false,
        suggestions: false,
        item: false,
      },

      quotation: {
        client: "",
        client_name: "",
        client_phone: "",
        iva: "19",
        discount: "0",
        subtotal: "0",
        totalDiscount: "0",
        totalIva: "0",
        total: "0",
      },
      quotationResults: {
        subtotal: "0",
        totalDiscount: "0",
        totalIva: "0",
        total: "0",
      },

      clients: [],

      item: {
        name: "",
        price: "",
      },

      items: [],

      suggestions: [],

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
    openPopUp: function (popUp) {
      this.popUps[popUp] = true;
    },

    openPopUpSuggestions: function (index) {
      this.popUps.suggestions = true;
      setTimeout(() => {
        let input = document.getElementById("suggestion");
        input.focus();
      }, 100);
      this.indexSuggestion = index;
      this.itemsQuotation[index].quantity = "";
      this.itemsQuotation[index].total = "";
    },

    openPopUpClientes: function (index) {
      this.popUps.clientes = true;
      setTimeout(() => {
        let input = document.getElementById("suggestion");
        input.focus();
      }, 100);
      this.indexSuggestion = index;
    },

    filterItems: function (suggestion) {
      let items = this.items;
      let filteredItems = items.filter((item) => {
        return item.name.toLowerCase().includes(suggestion.toLowerCase());
      });
      this.suggestions = filteredItems;

      if (suggestion === "") {
        this.suggestions = [];
      }
    },

    filterClients: function (suggestion) {
      let clients = this.clients;
      let filteredClients = clients.filter((client) => {
        return client.name.toLowerCase().includes(suggestion.toLowerCase());
      });
      this.suggestions = filteredClients;

      if (suggestion === "") {
        this.suggestions = [];
      }
    },

    setItemSuggestion: function (id, name, price) {
      this.itemsQuotation[this.indexSuggestion].item = id;
      this.itemsQuotation[this.indexSuggestion].name = name;
      this.itemsQuotation[this.indexSuggestion].price = price;

      this.popUps.suggestions = false;
      this.suggestions = [];
      this.suggestion = "";

      this.setTotalItemQuotation;
    },

    setClientSuggestion: function (id, name, phone) {
      this.quotation.client = id;
      this.quotation.client_name = name;
      this.quotation.client_phone = phone;

      this.popUps.clientes = false;
      this.suggestions = [];
      this.suggestion = "";
    },

    setIndexSuggestion: function (index) {
      this.indexSuggestion = index;
    },

    setTotalItemQuotation: function () {
      let price = this.itemsQuotation[this.indexSuggestion].price;
      let quantity = this.itemsQuotation[this.indexSuggestion].quantity;
      this.itemsQuotation[this.indexSuggestion].total = quantity * price;

      this.getResults();
    },

    editItemName: function (e) {
      let button = e.target;
      let input = button.parentElement.parentElement.querySelector("input");
      input.focus();
      this.popUps.suggestions = false;
    },

    editClientName: function (e) {
      let button = e.target;
      let input = button.parentElement.parentElement.querySelector("input");
      input.focus();
      this.popUps.clientes = false;
    },

    closePopUp: function (popUp) {
      this.popUps[popUp] = false;
    },

    createItemQuotation: function () {
      let itemQuotation = {
        quotation: "",
        item: "",
        name: "",
        price: "",
        quantity: "",
        total: "",
      };
      this.itemsQuotation.push(itemQuotation);
    },
    priceToString: function (price) {
      if (price != null && price != undefined) {
        return price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
      }
    },

    processCreateItem: function () {
      itemServices.createItem(this.item).then((result) => {
        itemServices.getItemsList().then((result) => {
          this.items = result;
        });
        this.item = {
          name: "",
          price: "",
        };
      });
    },

    // methods for the form
    processCreateQuotation: function () {
      quotationServices.createQuotation(this.quotation).then((result) => {
        this.errors.error_createQuotation = false;
        this.quotation = {
          client: "",
          client_name: "",
          client_phone: "",
          iva: "19",
          discount: "0",
          subtotal: "0",
          totalDiscount: "0",
          totalIva: "0",
          total: "0",
        };
        let quotationId = result.id;

        for (let i = 0; i < this.itemsQuotation.length; i++) {
          let itemQuotation = this.itemsQuotation[i];
          itemQuotation.quotation = quotationId;
          itemQuotationServices
            .createItemQuotation(itemQuotation)
            .then((result) => {
              console.log("Item quotation created");
              this.itemsQuotation = [];
              for (let i = 0; i < 2; i++) {
                this.createItemQuotation();
              }
              this.errors.error_createQuotation = false;
            });
        }

        this.errors.error_createQuotation = false;
        this.closePopUp("quotation");
        quotationServices.getQuotationsList().then((result) => {
          this.quotations = result;
        });
      });
    },

    processCreateItemsQuotation: function () {
      this.itemsQuotation.forEach((itemQuotation) => {
        console.log(itemQuotation);
      });
    },

    // generar totales
    getResults: function () {
      let subtotal = 0;
      let totalDiscount = 0;
      let totalIva = 0;
      let total = 0;

      let iva = this.quotation.iva;
      let discount = this.quotation.discount;

      for (let i = 0; i < this.itemsQuotation.length; i++) {
        let itemQuotation = this.itemsQuotation[i];
        subtotal += itemQuotation.total;
      }

      totalDiscount = subtotal * (discount / 100);

      totalIva = subtotal * (iva / 100);

      total = subtotal - totalDiscount + totalIva;

      this.quotationResults.subtotal = subtotal;
      this.quotationResults.totalDiscount = totalDiscount;
      this.quotationResults.totalIva = totalIva;
      this.quotationResults.total = total;

      console.log(this.quotationResults);
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

    clientServices.getClientsList().then((result) => {
      this.clients = result;
    });

    for (let i = 0; i < 1; i++) {
      this.createItemQuotation();
    }
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
@import "../assets/css/common/suggestion.css";
@import "../assets/css/base/base.css";
@import "../assets/css/common/table.css";
@import "../assets/css/common/tableResults.css";
</style>