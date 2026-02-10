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

export function scanDocument() {
  return request("/scan", {
    method: "POST",
    body: JSON.stringify({}),
  });
}

export function savePolicyDraft(payload) {
  return request("/payment/draft-save", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function initPayment(payload) {
  // payload: { policy_id, session_id, idempotency_key }
  return request("/payment/init", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function getPaymentStatus(sessionId) {
  return request(`/payment/status/${sessionId}`, { method: "GET" });
}

export async function downloadPolicyById(policyId) {
  const r = await fetch(`${BASE}/policy/download/${policyId}`, {
    method: "GET",
  });
  if (!r.ok) {
    const text = await r.text().catch(() => "");
    throw new Error(text || `HTTP ${r.status} ${r.statusText}`);
  }
  return r.blob();
}

export function scanPassportBeorg(imagesBase64, withRegistration = true) {
  return request("/scan/beorg-passport", {
    method: "POST",
    body: JSON.stringify({
      images: imagesBase64,
      with_registration: withRegistration,
    }),
  });
}
