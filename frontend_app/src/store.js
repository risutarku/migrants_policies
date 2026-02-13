// src/store.js
import { createPinia, defineStore } from "pinia";
export const pinia = createPinia();

export const useFlowStore = defineStore("flow", {
  state: () => ({
    lang: "ru",
    policyVariant: "basic", // basic|extended

    // ➜ данные из сканера / формы
    formData: {
      first_name: "",
      last_name: "",
      middle_name: "",
      sex: "", // 'male' | 'female'
      birthday: "", // yyyy-mm-dd (HTML <input type=date>)
      passport_series: "",
      passport_number: "",
      passport_issue_date: "",
      passport_expiry_date: "",
      passport_issuer: "",
    },
    formPolicy: {
      title: "",
      price: 1500,
    },
    formContacts: {
      phone_number: "",
      email: "",
    },
    sessionId: null,
    txId: null,
    arrived_for_hire: false,
    employeeTabNumber: "",
    policyId: null,
  }),
});
