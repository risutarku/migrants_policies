import { createI18n } from 'vue-i18n'
import ru from './i18n/locales/ru.json'

// 1. Список языков (добавил en для примера)
export const SUPPORTED = [
  { code: 'ru', label: 'Русский'   },
  { code: 'en', label: 'English'   },
  { code: 'kk', label: 'Қазақша'   },
  { code: 'uz', label: 'O‘zbekcha' },
  { code: 'ky', label: 'Кыргызча'  },
  { code: 'tg', label: 'Тоҷикӣ'    },
  { code: 'az', label: 'Azərbaycan'},
  { code: 'hy', label: 'Հայերեն'   },
  { code: 'ro', label: 'Română'    },
  { code: 'ka', label: 'ქართული'  },
]

// 2. Базовый экземпляр
export const i18n = createI18n({
  legacy: false,
  locale: 'ru',
  fallbackLocale: 'ru',
  messages: { ru },
})

// 3. Динамический импорт остальных переводов
//    Путь должен совпадать с тем, откуда вы взяли ru.json
const loaders = import.meta.glob('./i18n/locales/*.json')

export async function setLocale(code) {
  // если ещё не загружен файл — тащим его:
  if (!i18n.global.availableLocales.includes(code)) {
    const load = loaders[`./i18n/locales/${code}.json`]
    if (!load) return            // файла нет — тихо выходим
    const mod = await load()     // dynamic import
    i18n.global.setLocaleMessage(code, mod.default)
  }

  // переключаем локаль
  i18n.global.locale.value = code
  localStorage.setItem('lang', code)
}

// 4. Восстанавливаем сохранённый язык при старте
const saved = localStorage.getItem('lang')
if (saved && saved !== 'ru') setLocale(saved)
