import { createRouter, createWebHistory } from "vue-router";

export const routes = [
  {
    path: "/",
    name: "welcome",
    component: () => import("./pages/Welcome.vue"),
  },
  {
    path: "/scan",
    name: "scan",
    component: () => import("./pages/ScanDocument.vue"),
  },
  {
    path: "/edit",
    name: "edit",
    component: () => import("./pages/EditForm.vue"),
  },
  {
    path: "/payment_init",
    name: "payment_init",
    component: () => import("./pages/PaymentInit.vue"),
  },
  {
    path: "/payment_success",
    name: "payment_success",
    component: () => import("./pages/PaymentSuccess.vue"),
  },
  {
    path: "/choose_policy",
    name: "choose_policy",
    component: () => import("./pages/ChoosePolicy.vue"),
  },
  {
    path: "/contact_info",
    name: "contact_info",
    component: () => import("./pages/ContactInfo.vue"),
  },
];

export const router = createRouter({
  history: createWebHistory(),
  routes,
});
