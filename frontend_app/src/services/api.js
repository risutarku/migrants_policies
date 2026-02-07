// src/services/api.js
// const BASE = 'http://localhost:8000'   // поправь, если бек слушает иначе
export const BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

async function request(path, options = {}) {
  const r = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });

  if (!r.ok) {
    const text = await r.text().catch(() => "");
    throw new Error(text || `HTTP ${r.status} ${r.statusText}`);
  }

  // некоторые ответы могут быть пустыми, но у тебя везде json
  return r.json();
}

export function scanDocument(point) {
  return request("/scan", {
    method: "POST",
    body: JSON.stringify({ point }),
  });
}

export function submitForm(data) {
  return request("/user/register", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export function initPayment(payload) {
  return request("/payment/init", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function getPaymentStatus(sessionId) {
  return request(`/payment/status/${sessionId}`, { method: "GET" });
}

export function getPolicyQuote(payload) {
  return request("/policy/quote", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function downloadPolicyXlsxFromQuote(quote) {
  const r = await fetch(`${BASE}/policy/generate-xlsx-from-quote`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(quote),
  });
  if (!r.ok) {
    const text = await r.text().catch(() => "");
    throw new Error(text || `HTTP ${r.status}`);
  }
  return r.blob();
}
