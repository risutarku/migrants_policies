// src/store.js
import { createPinia, defineStore } from 'pinia'
export const pinia = createPinia()

export const useFlowStore = defineStore('flow', {
  state: () => ({
    lang: 'ru',
    point: null,

    // ➜ данные из сканера / формы
    formData: {
      name:              '',
      last_name:         '',
      middle_name:       '',
      sex:               '',          // 'male' | 'female'
      birthday:          '',          // yyyy-mm-dd (HTML <input type=date>)
      passport_series:   '',
      passport_number:   '',
      passport_issue_date:    '',
      passport_expiry_date:   '',
      passport_issuer:   '', 
    },
    formPolicy: {
      title: '',
      price: 0,
    },
    formContacts: {
      phone_number: '',
      email: '',
    },
    sessionID: null,
    txId: null,
  }),
})
