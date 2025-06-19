// // yyyy-mm-dd  ->  dd:mm:yy
// function isoToDmyYY(iso) {
//   if (!iso) return null
//   const [y, m, d] = iso.split('-')
//   return `${d}:${m}:${y.slice(-2)}`
// }

// export function toBackend(data) {
//   return {
//     'Name':               data.name,
//     'Last name':          data.last_name,
//     'middle name':        data.middle_name || null,
//     'sex':                data.sex,                       // male / female
//     'birthday':           isoToDmyYY(data.birthday),
//     'passport series':    Number(data.passport_series),
//     'passport number':    Number(data.passport_number),
//     'passport issue date':isoToDmyYY(data.passport_issue),
//     'passport expiry date': isoToDmyYY(data.passport_expiry),
//     'passport issuer':    data.passport_issuer,
//     // create date заполняет backend (есть default_factory)
//   }
// }
import { v4 as uuid } from 'uuid'

const dmy = iso => {
  if (!iso) return null
  const [y, m, d] = iso.split('-')
  return `${d}:${m}:${y.slice(-2)}`
}

export function makeInitPayload(form, amount) {
  return {
    // backend сгенерирует, но пусть будет явный sid
    session_id: uuid(),
    idempotency_key: uuid(),          // защита от повторных кликов
    amount,
    user: {
      'name'               : form.name,
      'last_name'          : form.last_name,
      'middle_name'        : form.middle_name || null,
      'sex'                : form.sex,
      'birthday'           : dmy(form.birthday),
      'passport_series'    : Number(form.passport_series),
      'passport_number'    : Number(form.passport_number),
      'passport_issue_date' : dmy(form.passport_issue_date),
      'passport_expiry_date' : dmy(form.passport_expiry_date),
      'passport_issuer'    : form.passport_issuer,
    },
  }
}
