// src/services/api.js
const BASE = 'http://localhost:8000'   // поправь, если бек слушает иначе
export const api = axios.create({ BASE });

export async function scanDocument(point) {
  const r = await fetch(`${BASE}/scan`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ point }),
  })
  if (!r.ok) throw new Error('scan error')
  return r.json()
}

export async function submitForm(data) {
  const r = await fetch(`${BASE}/user/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
  if (!r.ok) throw new Error('submit error')
  return r.json()
}

export async function initPayment(payload) {
  const r = await fetch(`${BASE}/payment/init`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
  if (!r.ok) throw new Error('initPayment error')
  return r.json()                      // { session_id, amount, currency }
}

export async function getPaymentStatus(sessionId) {
  const r = await fetch(`${BASE}/payment/status/${sessionId}`)
  if (!r.ok) throw new Error('status error')
  return r.json()                      // { status, tx_id }
}