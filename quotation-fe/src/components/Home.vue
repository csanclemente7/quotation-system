<template>
  <div class="home">
    <!-- loader -->
    <div class="dot-elastic"></div>
    <div class="home-data">
      <h1 class="home__subtitle">
        <img src="../assets/img/logo.png" alt="" />&nbsp;| Cotizaciones
      </h1>
      <div class="button-container">
        <button v-on:click="openPopUp('quotation')" class="button blue">
          Nueva Cotización
        </button>

        <button v-on:click="openPopUp('item')" class="button">Insumos</button>
      </div>

      <div class="grid-container-menu">
        <div class="input-container grid-menu-search">
          <!-- SECTION SEARCH FILTER -->
          <form>
            <input
              type="search"
              placeholder="Buscar..."
              id="input_search"
              v-model="filterSearch"
              v-on:input="filterBySearchInput"
              autocomplete="off"
            />
            <button
              type="button"
              aria-label="submit form"
              v-on:click="filterBySearchInput"
            >
              <li class="fas fa-search"></li>
            </button>
          </form>
        </div>

        <div class="input-container grid-menu-clientes">
          <button class="button">Clientes</button>
        </div>
      </div>

      <!--  QUOTATIONS TABLE -->
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
            v-for="quotation in paginatedData"
            :key="quotation"
            id="table_row"
            v-on:click="openPopUpUpdateQuotation('updateQuotation', quotation)"
          >
            <td>{{ quotation.id }}</td>
            <td>{{ quotation.date }}</td>
            <td>{{ quotation.client_name }}</td>
            <td>${{ priceToString(quotation.total) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="pagination-container">
      <nav aria-label="Page navigation example">
        <ul class="pagination">
          <li class="page-item">
            <a class="page-link" v-on:click="getPreviousPage()">Anterior</a>
          </li>
          <li
            v-for="page in pagination.totalPages(quotations.length)"
            :key="page"
            v-on:click="getDataPage(page, quotations)"
            class="page-item"
          >
            <a class="page-link" v-if="page != actualPage">{{ page }}</a>
            <div class="page-item active" aria-current="page">
              <span class="page-link" v-if="page === actualPage">{{
                actualPage
              }}</span>
            </div>
          </li>

          <li class="page-item">
            <a class="page-link" v-on:click="getNextPage()">Siguiente</a>
          </li>
        </ul>
      </nav>
    </div>
  </div>
  <!-- LOADER -->
  <div class="lds-spinner" v-if="startLoader || !totalInitialDataResults === 3">
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
    <!--- POPUP CREATE QUOTATION -->
    <div class="popup" v-if="popUps.quotation">
      <div class="popup-close-container">
        <div class="popup_close" v-on:click="closePopUp('quotation')">
          <svg
            width="25"
            height="25"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            stroke="var(--link-red-light)"
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
              type="number"
              name="iva"
              id="iva"
              class="input"
              v-on:input="setTotalItemQuotation"
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
              type="number"
              name="descuento"
              id="descuento"
              class="input"
              v-on:input="setTotalItemQuotation"
              v-model="quotation.discount"
              maxlength="7"
              required
            />
            <label class="input-label" for="descuento">% Descuento</label>
            <span class="input-message-error">Este campo no es valido</span>
          </div>

          <!-- button set items -->
          <div class="input-container add-items-manually">
            <button
              class="button"
              type="button"
              aria-label="submit form"
              v-on:click="setItemsQuotationManually('quotation')"
            >
              <i class="fas fa-plus"></i>
              &nbsp;Agregar Items
            </button>
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
              type="number"
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
              type="number"
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

          <!-- delete button -->
          <div class="input-container delete">
            <button
              class="delete-button"
              type="button"
              aria-label="submit form"
              v-on:click="deleteItemQuotation(index)"
            >
              <!-- delete icon -->
              <li class="fa fa-trash"></li>
            </button>
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
              <tr v-if="quotation.discount > 0">
                <td>Descuento {{ quotation.discount }}%</td>
                <td>${{ priceToString(quotationResults.totalDiscount) }}</td>
              </tr>
              <tr>
                <td>Iva {{ quotation.iva }}%</td>
                <td>${{ priceToString(quotationResults.totalIva) }}</td>
              </tr>
              <tr>
                <td>Total</td>
                <td>${{ priceToString(quotationResults.total) }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="input-container">
          <button class="button" type="submit">
            <i class="fas fa-download"></i>
            &nbsp;Generar Cotización
          </button>
          <div class="lds-ripple" v-if="downloadExecute">
            <div></div>
            <div></div>
          </div>
        </div>
      </form>
    </div>

    <!--- POPUP UPDATE QUOTATION -->
    <div class="popup popup-update-quotation" v-if="popUps.updateQuotation">
      <div class="popup-close-container">
        <div class="popup_close" v-on:click="closePopUp('updateQuotation')">
          <svg
            width="25"
            height="25"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            stroke="var(--link-red-light)"
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
        <img src="../assets/img/quotation_img.png" alt="" />&nbsp; Actualizar
        Cotización
      </h1>

      <!--- FORM -->
      <form
        v-on:submit.prevent="processUpdateQuotation"
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
              v-model="quotationUpdate.client_name"
              v-on:focus="openPopUpClientes(index)"
              autoComplete="off"
              required
            />
            <label class="input-label" for="cliente">Cliente</label>
            <button
              class="editbtn"
              type="button"
              aria-label="submit form"
              v-if="quotationUpdate.client_name != ''"
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
              v-on:input="setTotalItemQuotationUpdate"
              v-model="quotationUpdate.iva"
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
              v-on:input="setTotalItemQuotationUpdate"
              v-model="quotationUpdate.discount"
              maxlength="7"
              required
            />
            <label class="input-label" for="descuento">% Descuento</label>
            <span class="input-message-error">Este campo no es valido</span>
          </div>

          <!-- button set items -->
          <div class="input-container add-items-manually">
            <button
              class="button"
              type="button"
              aria-label="submit form"
              v-on:click="setItemsQuotationManually('quotationUpdate')"
            >
              <i class="fas fa-plus"></i>
              &nbsp;Agregar Items
            </button>
          </div>
        </div>
        <div
          class="row-form"
          v-for="(itemQuotationUpdate, index) in itemsQuotationUpdate"
          :key="index"
        >
          <div class="input-container item">
            <input
              type="text"
              name="item"
              id="item"
              class="input"
              v-model="itemQuotationUpdate.name"
              v-on:focus="openPopUpSuggestionsUpdate(index)"
              autocomplete="off"
              required
            />

            <label class="input-label" for="item">Item</label>
            <button
              class="editbtn"
              type="button"
              aria-label="submit form"
              v-if="itemQuotationUpdate.item != ''"
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
              v-model="itemQuotationUpdate.price"
              v-on:focus="setIndexSuggestionUpdate(index)"
              v-on:input="setTotalItemQuotationUpdate"
              :disabled="itemQuotationUpdate.item === ''"
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
              v-model="itemQuotationUpdate.quantity"
              v-on:focus="setIndexSuggestionUpdate(index)"
              v-on:input="setTotalItemQuotationUpdate"
              :disabled="itemQuotationUpdate.price === ''"
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
              v-model="itemQuotationUpdate.total"
              autocomplete="off"
              required
              disabled
            />
            <label class="input-label" for="total">Total</label>
            <span class="input-message-error">Este campo no es valido</span>
          </div>

          <!-- delete button -->
          <div class="input-container delete">
            <button
              class="delete-button"
              type="button"
              aria-label="submit form"
              v-on:click="deleteItemQuotationUpdate(itemQuotationUpdate, index)"
            >
              <!-- delete icon -->
              <li class="fa fa-trash"></li>
            </button>
          </div>
        </div>
        <!-- BOTON AGREGAR ITEM -->
        <button
          class="button add-item"
          v-on:click="createItemQuotationUpdate"
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
                <td>${{ priceToString(quotationUpdateResults.subtotal) }}</td>
              </tr>
              <tr v-if="quotationUpdate.discount > 0">
                <td>Descuento {{ quotationUpdate.discount }}%</td>
                <td>
                  ${{ priceToString(quotationUpdateResults.totalDiscount) }}
                </td>
              </tr>
              <tr>
                <td>Iva {{ quotationUpdate.iva }}%</td>
                <td>${{ priceToString(quotationUpdateResults.totalIva) }}</td>
              </tr>
              <tr>
                <td>Total</td>
                <td>${{ priceToString(quotationUpdateResults.total) }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="input-container">
          <button class="button" type="submit">
            <i class="fas fa-download"></i>
            &nbsp;Descargar Cotización
          </button>
        </div>

        <div class="input-container">
          <button
            class="button delete-button"
            type="button"
            v-on:click="processDeleteQuotation(idQuotationToUpdate)"
          >
            <i class="fas fa-trash"></i>
            Eliminar Cotización
          </button>
        </div>
      </form>
    </div>

    <!--- POP UP CREATE ITEM -->
    <div class="popup" v-if="popUps.item">
      <div class="popup-close-container">
        <div class="popup_close" v-on:click="closePopUp('item')">
          <svg
            width="25"
            height="25"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            stroke="var(--link-red-light)"
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
      <form
        class="formulario item-create-form"
        v-on:submit.prevent="processCreateItem"
      >
        <div class="header-form">
          <div class="input-container name">
            <input
              type="text"
              name="name"
              id="name"
              class="input"
              v-model="item.name"
              maxlength="70"
              autocomplete="off"
              required
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
              autocomplete="off"
              required
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
      <table class="custom-responsiva-two">
        <thead>
          <tr>
            <th>Item</th>
            <th>Precio</th>
          </tr>
        </thead>
        <tbody>
          <!--- problema a resolver -->
          <tr v-for="item in items" :key="item" id="table_row delete-custom">
            <td v-on:click="openPopUpItemUpdate('itemUpdate', item)">
              {{ item.name }}
            </td>
            <td v-on:click="openPopUpItemUpdate('itemUpdate', item)">
              ${{ priceToString(item.price) }}
            </td>
            <!-- delete button -->
            <td>
              <button
                class="delete-button"
                type="button"
                aria-label="submit form"
                v-on:click="processDeleteItemUpdate(items, item)"
              >
                <!-- delete icon -->
                <li class="fa fa-trash"></li>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <!--- finish pop up create item -->

    <!--- POP UP UPDATE ITEM -->
    <div class="popup popup-item-update" v-if="popUps.itemUpdate">
      <div class="popup-close-container">
        <div class="popup_close" v-on:click="closePopUp('itemUpdate')">
          <svg
            width="25"
            height="25"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            stroke="var(--link-red-light)"
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
      <form
        action=""
        class="form-container"
        v-on:submit.prevent="processUpdateItem"
      >
        <div class="input-container suggestion-container">
          <input
            type="text"
            name="item"
            id="itemUpdateName"
            class="input"
            v-model="itemToUpdate.name"
            autocomplete="off"
            required
          />
          <label class="input-label" for="suggestion"> Item </label>
          <span class="input-message-error">Este campo no es valido</span>
        </div>
        <div class="input-container suggestion-container">
          <input
            type="text"
            name="price"
            id="itemUpdatePrice"
            class="input"
            v-model="itemToUpdate.price"
            autocomplete="off"
            required
          />
          <label class="input-label" for="suggestion"> Precio </label>
          <span class="input-message-error">Este campo no es valido</span>
        </div>
        <button class="button" type="submit">Actualizar</button>
      </form>
    </div>

    <!--- POP UP SUGGESTIONS -->
    <div class="popup popup-suggestions" v-if="popUps.suggestions">
      <div class="popup-close-container">
        <div class="popup_close" v-on:click="closePopUp('suggestions')">
          <svg
            width="25"
            height="25"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            stroke="var(--link-red-light)"
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

    <!--- POP UP SUGGESTIONS UPDATE QUOTATION -->
    <div class="popup popup-suggestions" v-if="popUps.suggestionsUpdate">
      <div class="popup-close-container">
        <div class="popup_close" v-on:click="closePopUp('suggestionsUpdate')">
          <svg
            width="25"
            height="25"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            stroke="var(--link-red-light)"
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
          v-model="suggestionUpdate"
          v-on:focus="openPopUp('suggestionsUpdate')"
          v-on:input="filterItems(suggestionUpdate)"
          autocomplete="off"
        />
        <label class="input-label" for="suggestionUpdate"> Buscar Item </label>
        <span class="input-message-error">Este campo no es valido</span>

        <div
          class="suggestion"
          v-for="(item, index) in suggestions"
          :key="index"
        >
          <li
            v-on:click="setItemSuggestionUpdate(item.id, item.name, item.price)"
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

    <!--- POP UP CLIENTES -->
    <div class="popup popup-clientes" v-if="popUps.clientes">
      <div class="popup-close-container">
        <div class="popup_close" v-on:click="closePopUp('clientes')">
          <svg
            width="25"
            height="25"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            stroke="var(--link-red-light)"
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
        <label class="input-label" for="suggestion">
          Buscar Cliente Existente</label
        >
        <span class="input-message-error">Este campo no es valido</span>

        <div
          class="suggestion"
          v-for="(client, index) in suggestions"
          :key="index"
        >
          <li
            v-on:click="
              setClientSuggestion(
                client.id,
                client.name,
                client.phone,
                client.email,
                client.address,
                client.city
              )
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
        <div class="link-container" v-on:click="newClient = !newClient">
          <i class="fas fa-plus" v-if="!newClient">&nbsp;</i>
          <i class="fas fa-minus" v-if="newClient">&nbsp;</i>
          <a> Agregar Nuevo Cliente </a>
        </div>
      </div>

      <form
        class="client-form"
        v-if="newClient"
        v-on:submit.prevent="processCreateClient"
      >
        <div class="client-form-title">
          <h2>Agregar Nuevo Cliente</h2>
        </div>
        <div class="input-container client-name">
          <input
            type="text"
            name="name"
            id="name"
            class="input"
            v-model="client.name"
            autocomplete="off"
            required
          />
          <label class="input-label" for="name">Nombre</label>
          <span class="input-message-error">Este campo no es valido</span>
        </div>
        <div class="input-container client-city">
          <input
            type="text"
            name="city"
            id="city"
            class="input"
            v-model="client.city"
            autocomplete="off"
            required
          />
          <label class="input-label" for="phone">Ciudad</label>
          <span class="input-message-error">Este campo no es valido</span>
        </div>
        <div class="input-container client-address">
          <input
            type="text"
            name="address"
            id="address"
            class="input"
            v-model="client.address"
            autocomplete="off"
          />
          <label class="input-label" for="email">Dirección</label>
          <span class="input-message-error">Este campo no es valido</span>
        </div>
        <div class="input-container client-email">
          <input
            type="text"
            name="email"
            id="email"
            class="input"
            v-model="client.email"
            autocomplete="off"
            required
          />
          <label class="input-label" for="address">Email</label>
          <span class="input-message-error">Este campo no es valido</span>
        </div>
        <div class="input-container client-phone">
          <input
            type="text"
            name="phone"
            id="phone"
            class="input"
            v-model="client.phone"
            autocomplete="off"
          />
          <label class="input-label" for="phone">Teléfono</label>
          <span class="input-message-error">Este campo no es valido</span>
        </div>

        <div class="button-container">
          <button class="button button-add-client" type="submit">
            Agregar
          </button>
        </div>
      </form>
    </div>
  </section>
</template>
<script>
import axios from "axios";
import swal from "sweetalert";
import { itemServices } from "../service/item-service";
import { quotationServices } from "../service/quotation-service";
import { clientServices } from "../service/client-service";
import { itemQuotationServices } from "../service/item-quotation-service";
import jsPDFInvoiceTemplate, {
  OutputType,
  jsPDF,
} from "jspdf-invoice-template";

import { pdfBlob } from "../service/pdf-blob";
import { pagination } from "../pagination";

export default {
  name: "Home",
  data: function () {
    return {
      pagination: pagination,
      paginatedData: [],
      actualPage: 1,
      companyData: {
        companyName: "Macris Refrigeración & Aire s.a.s",
        companyAddress: "Carrera 10 # 6-45 Buga Valle del Cauca",
        companyPhone: "(+57) 316 772 1984",
        companyEmail: "w.sanclemente@hotmail.com",
        companyWebsite: "www.macrisrefrigeracion.com",
      },

      email: localStorage.getItem("email") || "none",
      is_admin: false,
      name: "",
      startLoader: false,
      tableRow: "",
      success_message: "",
      counter: 0,
      form: null,
      suggestions: "",
      suggestionUpdate: "",
      indexSuggestion: 0,
      indexSuggestionUpdate: 0,
      newClient: false,
      downloadExecuted: false,
      totalInitialDataResults: 0,
      props: {},
      pdfObject: {},
      pdfObjectBlob: {},
      filterSearch: "",
      quotationsToFilter: [],

      errors: {
        error_createQuotation: false,
        error_message: "",
      },

      popUps: {
        clientes: false,
        quotation: false,
        suggestions: false,
        suggestionsUpdate: false,
        item: false,
        itemUpdate: false,
        updateQuotation: false,
      },

      quotation: {
        id: "",
        client: "",
        client_name: "",
        client_phone: "",
        client_city: "",
        client_address: "",
        client_email: "",
        iva: "19",
        discount: "0",
        subtotal: "0",
        totalDiscount: "0",
        totalIva: "0",
        total: "0",
        home: null,
      },

      quotationUpdate: {
        id: "",
        client: "",
        client_name: "",
        client_phone: "",
        client_city: "",
        client_address: "",
        client_email: "",
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

      quotationUpdateResults: {
        subtotal: "0",
        totalDiscount: "0",
        totalIva: "0",
        total: "0",
      },

      clients: [],

      client: {
        name: "",
        city: "",
        address: "",
        email: "",
        phone: "",
      },

      item: {
        id: "",
        name: "",
        price: "",
      },

      itemToUpdate: {
        id: "",
        name: "",
        price: "",
      },

      items: [],

      suggestions: [],

      suggestionsUpdate: [],

      quotations: [],

      itemsQuotation: [],

      idQuotationToUpdate: "",

      itemsQuotationUpdate: [],
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

    // filter methods
    filterBySearchInput: function () {
      this.filterSearch = this.filterSearch.toLowerCase();
      this.quotationsToFilter = localStorage.getItem("quotations")
        ? JSON.parse(localStorage.getItem("quotations"))
        : [];

      if (this.filterSearch != "") {
        this.paginatedData = this.quotationsToFilter.filter((quotation) => {
          return (
            quotation.id.toString().includes(this.filterSearch) ||
            quotation.date.toLowerCase().includes(this.filterSearch) ||
            quotation.client_name.toLowerCase().includes(this.filterSearch) ||
            quotation.total.toString().includes(this.filterSearch) ||
            this.priceToString(quotation.total).includes(this.filterSearch)
          );
        });
      } else {
        this.paginatedData = this.quotationsToFilter;
        this.actualPage = 1;
        this.paginatedData = pagination.getDataPage(
          this.actualPage,
          this.quotations
        );
      }
    },

    // pop ups
    openPopUp: function (popUp) {
      this.home = document.querySelector(".home");
      this.home.classList.add("parentDiv");
      this.popUps[popUp] = true;
    },

    openPopUpItemUpdate: function (popUp, item) {
      this.itemToUpdate = item;
      this.home = document.querySelector(".home");
      this.home.classList.add("parentDiv");
      this.popUps[popUp] = true;
    },
    openPopUpUpdateQuotation: function (popUp, quotation) {
      this.idQuotationToUpdate = quotation.id;
      this.home = document.querySelector(".home");
      this.home.classList.add("parentDiv");
      this.popUps[popUp] = true;
      this.quotationUpdate = quotation;
      let itemQuotationUpdate = {
        quotation: "",
        item: "",
        name: "",
        price: "",
        quantity: "",
        total: "0",
      };
      this.itemsQuotationUpdate = [];

      this.itemsQuotationUpdate = quotation.quotationItems.map((item) => {
        return Object.assign({
          id: item.id,
          quotation: quotation.id,
          item: item.item_id,
          name: item.name,
          price: item.price,
          quantity: item.quantity,
          total: item.total,
        });
      });

      this.getResultsUpdate();
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
    openPopUpSuggestionsUpdate: function (index) {
      this.popUps.suggestionsUpdate = true;
      setTimeout(() => {
        let input = document.getElementById("suggestion");
        input.focus();
      }, 100);
      this.indexSuggestionUpdate = index;
      this.itemsQuotationUpdate[index].quantity = "";
      this.itemsQuotationUpdate[index].total = "";
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

    setItemSuggestionUpdate: function (id, name, price) {
      this.itemsQuotationUpdate[this.indexSuggestionUpdate].item = id;
      this.itemsQuotationUpdate[this.indexSuggestionUpdate].name = name;
      this.itemsQuotationUpdate[this.indexSuggestionUpdate].price = price;

      this.popUps.suggestionsUpdate = false;
      this.suggestions = [];
      this.suggestionUpdate = "";

      this.setTotalItemQuotationUpdate;
    },

    setClientSuggestion: function (id, name, phone, email, address, city) {
      this.quotation.client = id;
      this.quotation.client_name = name;
      this.quotation.client_phone = phone;
      this.quotation.client_email = email;
      this.quotation.client_address = address;
      this.quotation.client_city = city;

      this.popUps.clientes = false;
      this.suggestions = [];
      this.suggestion = "";
    },

    setIndexSuggestion: function (index) {
      this.indexSuggestion = index;
    },

    setIndexSuggestionUpdate: function (index) {
      this.indexSuggestionUpdate = index;
    },

    setTotalItemQuotation: function () {
      if (this.indexSuggestion != undefined) {
        let price = this.itemsQuotation[this.indexSuggestion].price;
        let quantity = this.itemsQuotation[this.indexSuggestion].quantity;
        this.itemsQuotation[this.indexSuggestion].total = price * quantity;
        if (price != undefined && quantity != undefined) {
          this.getResults();
        }
      }
    },

    setTotalItemQuotationUpdate: function () {
      if (this.indexSuggestionUpdate != undefined) {
        let price = this.itemsQuotationUpdate[this.indexSuggestionUpdate].price;
        let quantity =
          this.itemsQuotationUpdate[this.indexSuggestionUpdate].quantity;
        this.itemsQuotationUpdate[this.indexSuggestionUpdate].total =
          price * quantity;

        this.getResultsUpdate();
      }
    },

    editItemName: function (e) {
      let button = e.target;
      let input = button.parentElement.parentElement.querySelector("input");
      input.focus();
      this.popUps.suggestions = false;
      this.popUps.suggestionsUpdate = false;
    },

    editClientName: function (e) {
      let button = e.target;
      let input = button.parentElement.parentElement.querySelector("input");
      input.focus();
      this.popUps.clientes = false;
    },

    closePopUp: function (popUp) {
      this.popUps[popUp] = false;
      this.home.classList.remove("parentDiv");

      if (popUp === "quotation") {
        this.closePopUp("clientes");
        this.closePopUp("suggestions");
      }
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
    createItemQuotationUpdate: function () {
      let itemQuotation = {
        quotation: "",
        item: "",
        name: "",
        price: "",
        quantity: "",
        total: "",
      };
      this.itemsQuotationUpdate.push(itemQuotation);
    },

    deleteItemQuotation: function (index) {
      this.itemsQuotation.splice(index, 1);
      this.getResults();
    },

    deleteItemQuotationUpdate: function (itemQuotationUpdate, index) {
      swal({
        title: "¿Estás seguro?",
        text: "Una vez eliminado, no podrás recuperar este registro",
        icon: "warning",
        buttons: true,
        dangerMode: true,
      }).then((willDelete) => {
        if (willDelete) {
          this.itemsQuotationUpdate.splice(index, 1);
          this.getResultsUpdate();
          let itemId = itemQuotationUpdate.id;

          itemQuotationServices.deleteItemQuotation(itemId).then((response) => {
            console.log(response);
          });
        }
      });
    },
    priceToString: function (price) {
      if (price != null && price != undefined) {
        return price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
      }
    },

    processCreateItem: function () {
      this.startLoader = true;
      itemServices.createItem(this.item).then((result) => {
        itemServices.getItemsList().then((result) => {
          this.items = result;
          this.startLoader = false;
          this.item = {
            name: "",
            price: "",
          };
        });
      });
    },

    processUpdateItem: function () {
      itemServices.updateItem(this.itemToUpdate).then((result) => {
        this.errors.error_createItem = false;
        this.itemToUpdate = {
          name: "",
          price: "",
        };
        this.closePopUp("itemUpdate");
        itemServices.getItemsList().then((result) => {
          this.items = result;
          this.startLoader = false;
          this.item = {
            name: "",
            price: "",
          };
        });
      });
    },

    //Problema a resolver

    processDeleteItemUpdate: function (items, index) {
      swal({
        title: "¿Estás seguro?",
        text: "Una vez eliminado, no podrás recuperar este registro",
        icon: "warning",
        buttons: true,
        dangerMode: true,
      }).then((willDelete) => {
        if (willDelete) {
          this.items.splice(index, 1);
          let itemId = index.id;

          itemServices.deleteItem(itemId).then((response) => {
            console.log(response);
          });
        }
      });
    },
    //probando

    // methods for the form
    processCreateQuotation: function () {
      this.startLoader = true;
      quotationServices.createQuotation(this.quotation).then((result) => {
        let quotationId = result.id;
        this.quotation.id = quotationId;
        this.setProps("quotation");
        this.ejecutarDescarga();
        this.errors.error_createQuotation = false;
        this.quotation = {
          client: "",
          client_name: "",
          client_phone: "",
          client_city: "",
          client_address: "",
          client_email: "",
          client_phone: "",
          iva: "19",
          discount: "0",
          subtotal: "0",
          totalDiscount: "0",
          totalIva: "0",
          total: "0",
        };

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
              quotationServices.getQuotationsList().then((result) => {
                this.quotations = result;
                this.startLoader = false;
                this.filterSearch = "";
                this.paginatedData = pagination.getDataPage(
                  this.actualPage,
                  this.quotations
                );
              });
              this.errors.error_createQuotation = false;
            });
        }

        this.errors.error_createQuotation = false;
        this.closePopUp("quotation");
      });
    },

    processUpdateQuotation: function () {
      this.startLoader = true;
      quotationServices.updateQuotation(this.quotationUpdate).then((result) => {
        this.ejecutarDescarga();
        this.errors.error_createQuotation = false;
        this.quotationUpdate = {
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
        for (let i = 0; i < this.itemsQuotationUpdate.length; i++) {
          if (this.itemsQuotationUpdate[i].id === undefined) {
            let itemQuotation = this.itemsQuotationUpdate[i];
            itemQuotation.quotation = quotationId;
            itemQuotationServices
              .createItemQuotation(itemQuotation)
              .then((result) => {
                console.log("Item quotation created");
                this.errors.error_createQuotation = false;
              });
          } else {
            let itemQuotation = this.itemsQuotationUpdate[i];
            itemQuotation.quotation = quotationId;
            itemQuotationServices
              .updateItemQuotation(itemQuotation)
              .then((result) => {
                console.log("Item quotation updated");
                setTimeout(() => {
                  quotationServices.getQuotationsList().then((result) => {
                    this.quotations = result;
                    this.startLoader = false;
                    this.filterSearch = "";
                    this.paginatedData = pagination.getDataPage(
                      this.actualPage,
                      this.quotations
                    );
                  });
                }, 100);
                this.errors.error_createQuotation = false;
              });
          }
        }
        this.errors.error_createQuotation = false;
        this.closePopUp("updateQuotation");
      });
    },

    processDeleteQuotation: function (id) {
      this.startLoader = true;
      swal({
        title: "¿Estás seguro?",
        text: "Una vez eliminado, no podrás recuperar este registro",
        icon: "warning",
        buttons: true,
        dangerMode: true,
      }).then((willDelete) => {
        if (willDelete) {
          // si el usuario acepta eliminar el registro
          quotationServices.deleteQuotation(id).then((result) => {
            quotationServices.getQuotationsList().then((result) => {
              this.quotations = result;
              console.log(result);
              this.startLoader = false;
              this.filterSearch = "";
              this.paginatedData = pagination.getDataPage(
                this.actualPage,
                this.quotations
              );
            });
            this.closePopUp("updateQuotation");
          });
        }
      });
    },

    processCreateClient: function () {
      this.startLoader = true;
      clientServices.createClient(this.client).then((result) => {
        clientServices.getClientsList().then((result) => {
          this.clients = result;
        });
        this.client = {
          name: "",
          phone: "",
        };
        this.newClient = false;
        this.quotation.client = result.id;
        this.quotation.client_name = result.name;
        this.quotation.client_phone = result.phone;
        this.quotation.client_city = result.city;
        this.quotation.client_address = result.address;
        this.quotation.client_email = result.email;
        console.log(this.quotation);
        this.closePopUp("clientes");
        this.startLoader = false;
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

      totalIva = (subtotal - totalDiscount) * (iva / 100);

      total = subtotal - totalDiscount + totalIva;

      this.quotationResults.subtotal = subtotal;
      this.quotationResults.totalDiscount = totalDiscount;
      this.quotationResults.totalIva = totalIva;
      this.quotationResults.total = total;

      this.setProps("quotation");
    },

    // generar totales Actualizados
    getResultsUpdate: function () {
      let subtotal = 0;
      let totalDiscount = 0;
      let totalIva = 0;
      let total = 0;

      let iva = this.quotationUpdate.iva;
      let discount = this.quotationUpdate.discount;

      for (let i = 0; i < this.itemsQuotationUpdate.length; i++) {
        let itemQuotation = this.itemsQuotationUpdate[i];
        subtotal += itemQuotation.total;
      }

      totalDiscount = subtotal * (discount / 100);

      totalIva = (subtotal - totalDiscount) * (iva / 100);

      total = subtotal - totalDiscount + totalIva;

      this.quotationUpdateResults.subtotal = subtotal;
      this.quotationUpdateResults.totalDiscount = totalDiscount;
      this.quotationUpdateResults.totalIva = totalIva;
      this.quotationUpdateResults.total = total;

      this.setProps("quotationUpdate");
    },

    processUpdateItem: function () {
      this.startLoader = true;
      itemServices.updateItem(this.itemToUpdate).then((result) => {
        this.errors.error_createItem = false;
        this.itemToUpdate = {
          name: "",
          price: "",
        };
        this.closePopUp("itemUpdate");
        itemServices.getItemsList().then((result) => {
          this.items = result;
          this.startLoader = false;
        });
      });
    },

    // PDF DOWNLOADER

    generatePdf: function () {
      this.pdfObject = jsPDFInvoiceTemplate(this.props);

      console.log("Object created", this.pdfObject);
    },

    ejecutarDescarga: function () {
      this.generatePdf();
      this.downloadExecute = true;
    },

    setProps: function (typeQuotation) {
      let pdfData = [];
      let quotation = {};
      let quotationResults = {};
      if (typeQuotation === "quotation") {
        pdfData = this.itemsQuotation;
        quotation = this.quotation;
        quotationResults = this.quotationResults;
      } else if (typeQuotation === "quotationUpdate") {
        pdfData = this.itemsQuotationUpdate;
        quotation = this.quotationUpdate;
        quotationResults = this.quotationUpdateResults;
      }
      // date aaaa-mm-dd
      let dateToday = new Date();
      let date =
        dateToday.getFullYear() +
        "-" +
        (dateToday.getMonth() + 1) +
        "-" +
        dateToday.getDate();
      this.props = {
        outputType: OutputType.Save,
        returnJsPDFDocObject: true,
        fileName: `cotización-${quotation.client_name}-${this.dateToString(
          date
        )}`,
        orientationLandscape: false,
        compress: true,
        logo: {
          src: "https://i.ibb.co/z6qmdxq/logo.png",
          width: 53.33, //aspect ratio = width/height
          height: 26.66,
          margin: {
            top: 0, //negative or positive num, from the current position
            left: 20, //negative or positive num, from the current position
          },
        },
        business: {
          name: this.companyData.companyName,
          address: this.companyData.companyAddress,
          phone: this.companyData.companyPhone,
          email: this.companyData.companyEmail,
          website: this.companyData.companyWebsite,
          /* email_1: "info@example.al", */
        },
        contact: {
          label: "Dirigido a:",
          name: quotation.client_name,
          address: `Direccion: ${quotation.client_address}`,
          phone: `Teléfono: (+57) ${quotation.client_phone}`,
          email: `Email: ${quotation.client_email}`,
          otherInfo: "",
        },
        invoice: {
          label: "Cotización #: ",
          num: quotation.id,
          invDate: `Fecha ${this.dateToString(date)}`,
          /* invGenDate: "Invoice Date: 02/02/2021 10:17", */
          headerBorder: false,
          tableBodyBorder: false,
          header: [
            {
              title: "Producto o Servicio",
              style: {
                width: 80,
              },
            },
            {
              title: "Precio",
              style: {
                width: 40,
              },
            },
            {
              title: "Cantidad",
              style: {
                width: 40,
              },
            },
            {
              title: "Total",
              style: {
                width: 40,
              },
            },
          ],
          table: Array.from(
            Array(pdfData.length),
            (quotation = pdfData, index) => [
              /*         index + 1, */
              `${quotation[index].name}`,
              `$ ${this.priceToString(quotation[index].price)}`,
              `${quotation[index].quantity}`,
              `$ ${this.priceToString(quotation[index].total)}`,
            ]
          ),
          invTotalLabel: "Subtotal:",
          invTotal: `$ ${this.priceToString(quotationResults.subtotal)}`,
          invCurrency: "",
          row1: {
            col1: `Descuento (${quotation.discount}%) :\nIva (${quotation.iva}%) :`,
            col2: `$ ${this.priceToString(
              quotationResults.totalDiscount
            )}\n$ ${this.priceToString(quotationResults.totalIva)}`,
            col3: "",
            style: {
              fontSize: 10, //optional, default 12
            },
          },
          row2: {
            col1: "\nTotal:",
            col2: `\n$ ${this.priceToString(quotationResults.total)}`,
            col3: "",
            style: {
              fontSize: 12, //optional, default 12
            },
          },

          invDescLabel: "Términos y condiciones",
          invDesc:
            "1. Todos los productos y servicios cuentan con garantía. \n2. Valido por 15 días a partir de la fecha de la cotización.",
        },
        footer: {
          text: "Si usted tiene alguna pregunta sobre esta cotización, por favor, póngase en contacto con nosotros\nCelular: 3167721984 | E-mail: w.sanclemente@hotmail.com	\nGracias por hacer negocios con nosotros!",
        },
        pageEnable: true,
        pageLabel: "Página",
      };
      /* pdfBlob.setProps(this.props, jsPDFInvoiceTemplate); */
    },

    setItemsQuotationManually: function (type) {
      swal("¿ Cuantos items desea agregar ?", {
        content: "input",
        buttons: ["Cancelar", "Aceptar"],
      }).then((value) => {
        console.log("value", value);
        if (isNaN(value)) {
          swal("No se puede agregar un valor no numerico", "", "error");

          return;
        } else if (value > 50) {
          swal("No se puede agregar mas de 50 items", "", "error");
          return;
        } else if (value < 1 && value !== "" && value !== null) {
          swal("No se puede agregar menos de 1 item", "", "error");
          return;
        } else if (value == null) {
          return;
        } else {
          if (type === "quotation") {
            for (let i = 0; i < parseInt(value); i++) {
              this.createItemQuotation();
            }
          } else if (type === "quotationUpdate") {
            for (let i = 0; i < parseInt(value); i++) {
              this.createItemQuotationUpdate();
            }
          }
        }
      });
    },
    // convert date AAAA-MM-DD to DD/MM/AAAA
    dateToString: function (date) {
      date = date.toString();
      if (date != null && date != undefined) {
        let dateArray = date.split("-").reverse();
        dateArray[1] =
          dateArray[1].length == 1 ? "0" + dateArray[1] : dateArray[1];
        dateArray[2] =
          dateArray[2].length == 1 ? "0" + dateArray[2] : dateArray[2];
        return dateArray.join("/");
      }
    },
    getInitialData: function () {
      itemServices.getItemsList().then((result) => {
        this.items = result;
        this.totalInitialDataResults += 1;
      });

      quotationServices.getQuotationsList().then((result) => {
        this.quotations = result;
        this.totalInitialDataResults += 1;
        this.getDataPage(this.actualPage, this.quotations);
      });

      clientServices.getClientsList().then((result) => {
        this.clients = result;
        this.totalInitialDataResults += 1;
      });
    },

    // PAGINATION FUNCTIONS

    // trae los datos paginados
    getDataPage: function (page, quotations) {
      this.filterSearch = ""; // borra el filtro
      this.actualPage = page;
      this.paginatedData = pagination.getDataPage(page, quotations);
    },

    // trae los datos de la página anterior
    getPreviousPage: function () {
      this.filterSearch = ""; // borra el filtro
      this.actualPage = pagination.getPreviousPage(this.actualPage);

      this.paginatedData = pagination.getDataPage(
        this.actualPage,
        this.quotations
      );
    },

    // trae los datos de la página siguiente
    getNextPage: function () {
      this.filterSearch = ""; // borra el filtro
      this.actualPage = pagination.getNextPage(
        this.actualPage,
        pagination.totalPages(this.quotations.length)
      );

      this.paginatedData = pagination.getDataPage(
        this.actualPage,
        this.quotations
      );
    },
  },

  created: function () {
    this.verifyAuth();
    this.name = localStorage.getItem("name") || "";
    this.is_admin = JSON.parse(localStorage.getItem("isAdmin")) || false;
    this.createItemQuotation();

    this.getInitialData();

    for (let i = 0; i < 1; i++) {
      this.createItemQuotation();
    }
  },
};
</script>
<style>
table .active {
  background-color: #007bbd;
  color: #ffffff;
}
.pagination-container {
  margin-top: 10px;
  cursor: pointer;
}
.home {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: absolute;
  width: 100%;
  z-index: 2;
  padding-bottom: 20px;
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
  font-size: 35px;
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
@import "../assets/css/common/grid-menu.css";
@import "../assets/css/common/inputs.css";
@import "../assets/css/common/button.css";
@import "../assets/css/common/links.css";
@import "../assets/css/common/suggestion.css";
@import "../assets/css/base/base.css";
@import "../assets/css/common/table.css";
@import "../assets/css/common/tableResults.css";
@import "../assets/css/common/lds-ripple.css";
</style>