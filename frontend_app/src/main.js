import { createApp } from 'vue'
import App            from './App.vue'
import { router }     from './router'
import { i18n }       from './i18n'     // ← именованный import
import { pinia }      from './store'
import './assets/tailwind.css'

createApp(App)
  .use(router)
  .use(i18n)
  .use(pinia)
  .mount('#app')
