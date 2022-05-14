<template>
  <div class="home">
    <div class="home-data">
      <h1 class="login__subtitle">
        <img src="../assets/img/home_img.png" alt="" />&nbsp; Lavadero App
      </h1>
      <div class="input-group-home">
        <button v-on:click="openPopUp('reporte')" class="btn-home-1">
          Nuevo reporte
        </button>
      </div>
    </div>
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
      popUps: {
        reporte: false,
        updateReporte: false,
      },
      reporte: {
        placa: "",
        tipo_vehiculo: "",
        servicio: "",
        auxiliar: "Pendiente",
        valor: "",
        pagado: false,
        nequi: false,
        observaciones: "",
      },
      filters: {
        filter: "",
        fecha: "",
        success_message: "",
        error_message: "",
      },

      reporteToUpdate: {},

      selects: {
        tiposVehiculo: [],
        servicios: [],
        auxiliares: [],
        auxiliaresReportados: [],
      },

      resultados: {
        totalIngresos: 0,
        reportesDia: [],
      },

      error_message: "",
      success_message: "",
      error_createReport: false,
      error_updateReport: false,
      reportes: [],
      allreportes: [],
      showAll: false,
      linkText: "Ver Todos",
      currentDatereportes: [],
      currentDate: "",
      index: 0,
      tableRow: "",
      CurrentReports: [],
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

    createReport: async function () {
      if (this.reporte.nequi) {
        this.reporte.pagado = true;
      }
      this.startLoader = true;
      if (
        localStorage.getItem("token_access") === null ||
        localStorage.getItem("token_refresh") === null
      ) {
        this.$emit("logOut");
        return;
      }
      await this.$emit("verifyToken"); // esto se utiliza para esperar a que la sección de comprobación y actualización delaccess token terminen, y que solo cuando hayan terminado

      let token = localStorage.getItem("token_access");
      let userId = jwt_decode(token).user_id.toString();
      axios
        .post(
          `https://quotation-system-be.herokuapp.com/reporte/${userId}`,
          this.reporte,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        )
        .then((response) => {
          swal("Reporte creado correctamente", "", "success");
          // clear inputs
          this.reporte = {
            tipo_vehiculo: "",
            servicio: "",
            auxiliar: "Pendiente",
            valor: "",
            pagado: false,
            nequi: false,
            observaciones: "",
          };
          this.closePopUp("reporte");
          this.allreportes = [];
          this.currentDatereportes = [];
          this.getReportes();
          this.startLoader = false;
        })
        .catch((error) => {
          console.log(error);
          if (error.response.status == "401") {
            this.error_message = "error de autenticación";
            this.error_createReport = true;
          } else if (error.response.status == "400") {
            this.error_message = "error de validación";
            this.error_createReport = true;
          } else if (error.response.status == "500") {
            this.error_message = "Error en el servidor";
            this.error_createReport = true;
          } else {
            this.error_message = "Error en el servidor";
            this.error_createReport = true;
          }
          this.startLoader = false;
        });
    },

    updateReport: async function () {
      if (this.reporteToUpdate.nequi) {
        this.reporteToUpdate.pagado = true;
      }
      this.startLoader = true;
      if (
        localStorage.getItem("token_access") === null ||
        localStorage.getItem("token_refresh") === null
      ) {
        this.$emit("logOut");
        return;
      }
      await this.$emit("verifyToken"); // esto se utiliza para esperar a que la sección de comprobación y actualización delaccess token terminen, y que solo cuando hayan terminado

      let token = localStorage.getItem("token_access");
      let userId = jwt_decode(token).user_id.toString();
      let reportId = this.reporteToUpdate.id;
      axios
        .put(
          `https://quotation-system-be.herokuapp.com/reporte/${userId}/${reportId}/update`,
          this.reporteToUpdate,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        )
        .then((response) => {
          /* swal("Actualizado correctamente", "", "success"); */
          // clear inputs
          this.reporteToUpdate = {};
          this.closePopUp("updateReporte");
          this.allreportes = [];
          this.currentDatereportes = [];
          this.getReportes();
          this.startLoader = false;
        })
        .catch((error) => {
          console.log(error);
          if (error.response.status == "401") {
            this.error_message = "error de autenticación";
            this.error_createReport = true;
          } else if (error.response.status == "400") {
            this.error_message = "error de validación";
            this.error_createReport = true;
          } else if (error.response.status == "500") {
            this.error_message = "Error en el servidor";
            this.error_createReport = true;
          } else {
            this.error_message = "Error en el servidor";
            this.error_createReport = true;
          }
          this.startLoader = false;
        });
    },

    deleteReport: async function () {
      this.startLoader = true;
      if (
        localStorage.getItem("token_access") === null ||
        localStorage.getItem("token_refresh") === null
      ) {
        this.$emit("logOut");
        return;
      }
      await this.$emit("verifyToken");

      let token = localStorage.getItem("token_access");
      let userId = jwt_decode(token).user_id.toString();
      let reportId = this.reporteToUpdate.id;
      axios
        .delete(
          `https://quotation-system-be.herokuapp.com/reporte/${userId}/${reportId}/delete`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        )
        .then((response) => {
          /* swal("Actualizado correctamente", "", "success"); */
          // clear inputs
          swal({
            text: "Reporte eliminado correctamente",
            timer: 1400,
            icon: "success",
            buttons: false,
            closeOnClickOutside: false,
          });
          this.reporteToUpdate = {};
          this.closePopUp("updateReporte");
          this.allreportes = [];
          this.currentDatereportes = [];
          this.getReportes();
          this.startLoader = false;
        })
        .catch((error) => {
          console.log(error);
          if (error.response.status == "401") {
            this.error_message = "error de autenticación";
            this.error_createReport = true;
          } else if (error.response.status == "400") {
            this.error_message = "error de validación";
            this.error_createReport = true;
          } else if (error.response.status == "500") {
            this.error_message = "Error en el servidor";
            this.error_createReport = true;
          } else {
            this.error_message = "Error en el servidor";
            this.error_createReport = true;
          }
          this.startLoader = false;
        });
    },

    getTiposVehiculo: async function () {
      this.startLoader = true;
      if (
        localStorage.getItem("token_access") === null ||
        localStorage.getItem("token_refresh") === null
      ) {
        return;
      }
      await this.$emit("verifyToken"); // esto se utiliza para esperar a que la sección de comprobación y actualización delaccess token terminen, y que solo cuando hayan terminado

      let token = localStorage.getItem("token_access");
      let userId = jwt_decode(token).user_id.toString();

      axios
        .get(
          `https://quotation-system-be.herokuapp.com/tipoVehiculos/${userId}`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        )
        .then((response) => {
          response.data.map((tipo) => {
            this.selects.tiposVehiculo.push(tipo.nombre);
          });

          this.startLoader = false;
        })

        .catch((error) => {
          console.log(error);
          this.startLoader = false;
        });
    },

    getServicios: async function () {
      this.startLoader = true;
      if (
        localStorage.getItem("token_access") === null ||
        localStorage.getItem("token_refresh") === null
      ) {
        return;
      }
      await this.$emit("verifyToken"); // esto se utiliza para esperar a que la sección de comprobación y actualización delaccess token terminen, y que solo cuando hayan terminado

      let token = localStorage.getItem("token_access");
      let userId = jwt_decode(token).user_id.toString();

      axios
        .get(`https://quotation-system-be.herokuapp.com/servicios/${userId}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        .then((response) => {
          response.data.map((servicio) => {
            this.selects.servicios.push(servicio.nombre);
          });

          this.startLoader = false;
        })

        .catch((error) => {
          console.log(error);
          this.startLoader = false;
        });
    },

    getAuxiliares: async function () {
      this.startLoader = true;
      if (
        localStorage.getItem("token_access") === null ||
        localStorage.getItem("token_refresh") === null
      ) {
        return;
      }
      await this.$emit("verifyToken"); // esto se utiliza para esperar a que la sección de comprobación y actualización delaccess token terminen, y que solo cuando hayan terminado

      let token = localStorage.getItem("token_access");
      let userId = jwt_decode(token).user_id.toString();

      axios
        .get(`https://quotation-system-be.herokuapp.com/auxiliares/${userId}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        .then((response) => {
          response.data.map((auxiliar) => {
            this.selects.auxiliares.push(auxiliar.nombre);
          });

          this.startLoader = false;
        })

        .catch((error) => {
          console.log(error);
          this.startLoader = false;
        });
    },

    getReportes: async function () {
      this.startLoader = true;
      if (
        localStorage.getItem("token_access") === null ||
        localStorage.getItem("token_refresh") === null
      ) {
        return;
      }
      await this.$emit("verifyToken"); // esto se utiliza para esperar a que la sección de comprobación y actualización delaccess token terminen, y que solo cuando hayan terminado

      let token = localStorage.getItem("token_access");
      let userId = jwt_decode(token).user_id.toString();

      axios
        .get(`https://quotation-system-be.herokuapp.com/reportes/${userId}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        .then((response) => {
          this.allreportes = response.data;
          this.index = 0;
          this.showAllReports();

          // reportes current date
          let currentDate = new Date().toLocaleDateString("es-CO");

          let currentDateArray = currentDate.split("/");

          currentDateArray[0] =
            currentDateArray[0].length == 1
              ? "0" + currentDateArray[0]
              : currentDateArray[0];
          currentDateArray[1] =
            currentDateArray[1].length == 1
              ? "0" + currentDateArray[1]
              : currentDateArray[1];
          currentDate = currentDateArray.join("/");
          this.currentDate = currentDate;
          this.allreportes.map((reporte) => {
            console.log(reporte.fecha);
            if (reporte.fecha == currentDate) {
              this.currentDatereportes.push(reporte);
            }
          });
          this.startLoader = false;
        })

        .catch((error) => {
          console.log(error);
          this.startLoader = false;
        });
    },

    // other methods

    loadCreateReport: function () {
      this.$router.push("createReport");
    },
    loadHistorial: function () {
      this.$router.push("historialGeneral");
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

    // pop ups
    openPopUp: function (popUp, reporte) {
      if (reporte != null) {
        this.reporteToUpdate = {
          id: reporte.id,
          placa: reporte.placa,
          tipo_vehiculo: reporte.tipo_vehiculo,
          servicio: reporte.servicio,
          auxiliar: reporte.auxiliar,
          valor: reporte.valor,
          pagado: reporte.pagado,
          nequi: reporte.nequi,
          observaciones: reporte.observaciones,
        };
      }
      this.popUps[popUp] = true;
    },
    closePopUp: function (popUp) {
      this.popUps[popUp] = false;
    },

    priceToString: function (price) {
      if (price != null && price != undefined) {
        return price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
      }
    },

    showAllReports: function () {
      const list = [this.allreportes, this.currentDatereportes];
      if (this.index == 0) {
        this.showAll = false;
        this.linkText = "Ver reportes de todas las fechas";
        this.index = 1;
        this.clearFilters();
      } else {
        this.showAll = true;
        this.linkText = "Ver reportes de hoy";
        this.index = 0;
      }
      this.reportes = list[this.index];
      setTimeout(() => {
        this.selects.auxiliaresReportados = [];
        this.reportes.map((reporte) => {
          if (
            !this.selects.auxiliaresReportados.includes(reporte.auxiliar) &&
            reporte.auxiliar != null &&
            reporte.auxiliar != undefined &&
            reporte.auxiliar != "" &&
            reporte.auxiliar != "Pendiente"
          ) {
            this.selects.auxiliaresReportados.push(reporte.auxiliar);
          }
        });
        this.generateDailyReport();
      }, 100);
    },

    changeColorTr: function () {
      let tableRow = document.getElementById("table_row");
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

    convertDateToLocal: function (date) {
      if (date != null || (date != undefined && date != "")) {
        // convert AAAA-MM-DD to DD/MM/AAAA
        let date_array = date.split("/");
        let day = date_array[0];
        let month = date_array[1];
        if (month == "01") {
          month = "enero";
        } else if (month == "02") {
          month = "febrero";
        } else if (month == "03") {
          month = "marzo";
        } else if (month == "04") {
          month = "abril";
        } else if (month == "05") {
          month = "mayo";
        } else if (month == "06") {
          month = "junio";
        } else if (month == "07") {
          month = "julio";
        } else if (month == "08") {
          month = "agosto";
        } else if (month == "09") {
          month = "septiembre";
        } else if (month == "10") {
          month = "octubre";
        } else if (month == "11") {
          month = "noviembre";
        } else if (month == "12") {
          month = "diciembre";
        }

        let year = date_array[2];
        let new_date = day + " de " + month + " de " + year;
        return new_date;
      } else {
        return "";
      }
    },

    // methods to filter the reports
    filterReports: function () {
      let filter = "";
      if (new Date(this.filters.filter) != "Invalid Date") {
        filter = this.dateToString(this.filters.filter);
      } else {
        filter = this.filters.filter;
      }

      if (this.showAll) {
        this.CurrentReports = this.allreportes;
      } else {
        this.CurrentReports = this.currentDatereportes;
      }
      if (filter == "todos") {
        this.filters.success_message = "Fitros quitados";
        setTimeout(() => {
          this.filters.success_message = "";
          this.filters.error_message = "";
        }, 1000);
        this.reportes = this.CurrentReports;
        this.generateDailyReport();
      } else {
        let filtered = this.CurrentReports.filter((reporte) => {
          return (
            reporte.tipo_vehiculo
              .toLowerCase()
              .includes(filter.toLowerCase()) ||
            reporte.fecha.includes(filter) ||
            reporte.servicio.toLowerCase().includes(filter.toLowerCase()) ||
            reporte.auxiliar.toLowerCase().includes(filter.toLowerCase()) ||
            reporte.valor.toLowerCase().includes(filter.toLowerCase()) ||
            reporte.observaciones.toLowerCase().includes(filter.toLowerCase())
          );
        });
        if (filtered.length > 0) {
          this.filters.error_message = "";
          this.filters.success_message = "Reportes filtrados";
          setTimeout(() => {
            this.filters.success_message = "";
            this.filters.error_message = "";
          }, 1000);
        } else {
          this.filters.error_message = "Sin resultados";
        }
        this.reportes = filtered;
        this.generateDailyReport();
      }
    },

    clearFilters: function () {
      this.filters.filter = "";
      this.filters.success_message = "";
      this.filters.error_message = "";
      this.reportes = this.CurrentReports;
    },

    // comprobate if list includes an object exactly the same
    arrayIncludes: function (list, obj) {
      for (let i = 0; i < list.length; i++) {
        if (
          list[i].servicio == obj.servicio &&
          list[i].tipo_vehiculo == obj.tipo_vehiculo
        ) {
          return true;
        }
      }
      return false;
    },

    quantityReportsByServieAndVehicle: function (servicio, tipoVehiculo) {
      let quantity = 0;
      this.reportes.map((reporte) => {
        if (
          reporte.servicio == servicio &&
          reporte.tipo_vehiculo == tipoVehiculo
        ) {
          quantity++;
        }
      });
      return quantity;
    },

    calculateTotalByServieAndVehicle: function (servicio, tipoVehiculo) {
      let total = 0;
      this.reportes.map((reporte) => {
        if (
          reporte.servicio == servicio &&
          reporte.tipo_vehiculo == tipoVehiculo
        ) {
          if (!reporte.valor == "") {
            total += parseInt(reporte.valor);
          } else {
            total += 0;
          }
        }
      });
      return total;
    },

    calculateTotal: function () {
      let total = 0;
      this.reportes.map((reporte) => {
        if (!reporte.valor == "") {
          total += parseInt(reporte.valor);
        } else {
          total += 0;
        }
      });
      this.resultados.totalIngresos = total;
    },

    // daily report
    generateDailyReport: function () {
      this.resultados.reportesDia = [];
      let reportes = [];
      if (this.showAll) {
        reportes = this.allreportes;
      } else {
        reportes = this.currentDatereportes;
      }
      let dailyReports = [];
      reportes.map((reporte) => {
        let object = {
          servicio: reporte.servicio,
          tipo_vehiculo: reporte.tipo_vehiculo,
          cantidad: this.quantityReportsByServieAndVehicle(
            reporte.servicio,
            reporte.tipo_vehiculo
          ),
          ingresos: this.calculateTotalByServieAndVehicle(
            reporte.servicio,
            reporte.tipo_vehiculo
          ),
        };
        if (!this.arrayIncludes(dailyReports, object)) {
          dailyReports.push(object);
        }
      });
      this.resultados.reportesDia = dailyReports;
      // sort alphabetically by servicio
      this.resultados.reportesDia.sort((a, b) => {
        if (a.servicio < b.servicio) {
          return -1;
        }
        if (a.servicio > b.servicio) {
          return 1;
        }
        return 0;
      });

      this.calculateTotal();
    },
  },

  created: function () {
    this.verifyAuth();
    this.name = localStorage.getItem("name") || "";
    this.is_admin = JSON.parse(localStorage.getItem("isAdmin")) || false;
    this.getTiposVehiculo();
    this.getServicios();
    this.getAuxiliares();
    this.getReportes();
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

@import "../assets/css/home/home-popUp.css";
@import "../assets/css/home/componentes/filters.css";
@import "../assets/css/home/componentes/inputs.css";
@import "../assets/css/home/componentes/button.css";
@import "../assets/css/home/componentes/checkbox.css";
@import "../assets/css/home/componentes/links.css";
@import "../assets/css/home/componentes/table.css";
@import "../assets/css/home/componentes/tableCounter.css";
@import "../assets/css/home/componentes/tableMobile.css";
@import "../assets/css/home/componentes/totales.css";
/* @import "../assets/css/home/componentes/tableMobileResponsive.css"; */
@import "../assets/css/home/base/base.css";
</style>