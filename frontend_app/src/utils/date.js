// utils/date.js
export const dmyToIso = (dmy) => {
  // "01:01:90" → "1990-01-01"
  if (!dmy) return ''
  const [d, m, y] = dmy.split(':')
  return `19${y}-${m}-${d}`   // <-- если 90-99 = 1990-1999; при 00-25 сделайте 20${y}
}

export const isoToDmy = (iso) => {
  // "1990-01-01" → "01:01:90"
  if (!iso) return null
  const [y, m, d] = iso.split('-')
  return `${d}:${m}:${y.slice(-2)}`
}
