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
            <th>Estado</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="reporte in reportes"
            :key="reporte"
            id="table_row"
            v-on:click="openPopUp('updateReporte', reporte)"
          >
            <td v-if="showAll">{{ reporte.fecha }}</td>
            <td>{{ reporte.placa }}</td>
            <td>{{ reporte.tipo_vehiculo }}</td>
            <td>{{ reporte.servicio }}</td>
            <td v-if="reporte.auxiliar != 'Pendiente'">
              {{ reporte.auxiliar }}
            </td>
            <td v-if="reporte.auxiliar === 'Pendiente'" class="pendiente">
              <li class="fa fa-exclamation-triangle"></li>
            </td>

            <td v-if="reporte.valor != ''">
              ${{ priceToString(reporte.valor) }}
            </td>
            <td v-if="reporte.valor === ''" class="pendiente">
              <div><li class="fa fa-exclamation-triangle"></li></div>
            </td>
            <td v-if="reporte.pagado || reporte.nequi" class="pagado">
              <li class="fa fa-check" v-if="!reporte.nequi"></li>
              <p v-if="reporte.nequi">Nequi</p>
            </td>
            <td v-if="!reporte.pagado && !reporte.nequi" class="debe">
              <li class="fa fa-exclamation-triangle"></li>
            </td>
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
              v-model="itemQuotation.name"
              v-on:focus="openPopUpSuggestions(index)"
              autocomplete="off"
            />

            <label class="input-label" for="item">Item</label>
            <button
              class="editbtn"
              type="submit"
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
              v-on:input="setTotalItemQuotation"
              :disabled="itemQuotation.item === ''"
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
              v-on:input="setTotalItemQuotation"
              :disabled="itemQuotation.price === ''"
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

        <div class="input-container">
          <button class="button" type="submit">Generar</button>
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
      suggestions: "",
      indexSuggestion: 0,

      errors: {
        error_createQuotation: false,
        error_message: "",
      },

      popUps: {
        quotation: false,
        suggestions: false,
        item: false,
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
      /* this.setItem(index); */
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

    setItemSuggestion: function (id, name, price) {
      this.itemsQuotation[this.indexSuggestion].item = id;
      this.itemsQuotation[this.indexSuggestion].name = name;
      this.itemsQuotation[this.indexSuggestion].price = price;

      this.popUps.suggestions = false;
      this.suggestions = [];
      this.suggestion = "";
    },

    setTotalItemQuotation: function () {
      let price = this.itemsQuotation[this.indexSuggestion].price;
      let quantity = this.itemsQuotation[this.indexSuggestion].quantity;
      this.itemsQuotation[this.indexSuggestion].total = quantity * price;
    },

    editItemName: function (e) {
      let button = e.target;
      let input = button.parentElement.parentElement.querySelector("input");
      input.focus();
      this.popUps.suggestions = false;
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
    for (let i = 0; i < 2; i++) {
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
</style>