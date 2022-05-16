import { createRouter, createWebHistory } from "vue-router";
import App from "./App.vue";
import LogIn from "./components/LogIn.vue";
import SignUp from "./components/SignUp.vue";
import Home from "./components/Home.vue";
import Quotation from "./components/Quotation.vue";
const routes = [
  {
    path: "/",
    name: "root",
    component: App,
  },
  {
    path: "/logIn",
    name: "logIn",
    component: LogIn,
  },
  {
    path: "/signUp",
    name: "signUp",
    component: SignUp,
  },
  {
    path: "/home",
    name: "home",
    component: Home,
  },
  {
    path: "/quotation",
    name: "quotation",
    component: Quotation,
  },
];
const router = createRouter({
  history: createWebHistory(),
  routes,
});
export default router;
