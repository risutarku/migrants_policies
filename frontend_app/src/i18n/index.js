import { createI18n } from 'vue-i18n'
import ru from './locales/ru.json'

export const SUPPORTED = [{ code: 'ru', label: 'Русский' }]

export const i18n = createI18n({
  legacy: false,
  locale: 'ru',
  fallbackLocale: 'ru',
  messages: { ru },
})

export async function setLocale(code) {
  if (!i18n.global.availableLocales.includes(code)) {
    const msgs = await import(/* @vite-ignore */ `./locales/${code}.json`)
    i18n.global.setLocaleMessage(code, msgs.default)
  }
  i18n.global.locale.value = code
}
