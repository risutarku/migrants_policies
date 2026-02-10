<script setup>
import { ref, computed } from "vue";
import { useI18n } from "vue-i18n";
import { useRouter } from "vue-router";
import { SUPPORTED as countries } from "@/i18n";
import { useFlowStore } from "@/store";

const router = useRouter();
const { t } = useI18n();
const flow = useFlowStore();

// email & phone input models
const selectedCountry = ref(countries[0].code);

// simple dial codes map (extend as needed)
const dialCodes = {
  ru: "+7",
  kk: "+7",
  uz: "+998",
  ky: "+996",
  tg: "+992",
  az: "+994",
  hy: "+374",
  ro: "+40",
  ka: "+995",
};

const phonePrefix = computed(() => dialCodes[selectedCountry.value] ?? "");

function changeCountry(code) {
  selectedCountry.value = code;
  // prepend prefix if отсутствует
  if (!phone.value.startsWith(phonePrefix.value)) {
    phone.value = phonePrefix.value;
  }
}

const email = computed({
  get: () => flow.formContacts.email,
  set: (v) => (flow.formContacts.email = v),
});
const phone = computed({
  get: () => flow.formContacts.phone_number,
  set: (v) => (flow.formContacts.phone_number = v),
});

function back() {
  router.back();
}

function forward() {
  router.push("/scan"); // заменить на реальный маршрут следующего шага
}
</script>

<template>
  <div
    class="flex flex-col items-center min-h-screen bg-gradient-to-b from-sky-50 to-white px-4 py-8"
  >
    <main
      class="flex flex-col items-center justify-center text-center space-y-6 max-w-2xl flex-1 w-full"
    >
      <!-- Logo -->
      <img
        src="/logo_ing.svg"
        alt="Ingosstrakh logo"
        class="w-60 h-auto my-6 ml-14 select-none pointer-events-none self-start"
      />
      <h1
        class="font-extrabold leading-tight text-3xl sm:text-4xl md:text-5xl whitespace-pre-line"
      >
        {{ t("contact_info.title") }}
      </h1>

      <label
        for="phone-input"
        class="block text-left w-full max-w-xl mt-4 mb-1 font-medium text-gray-700"
      >
        {{ t("contact_info.enter_email") }}
      </label>
      <!-- Email input -->
      <input
        v-model="email"
        type="email"
        :placeholder="'myemail@ingosstrah.ru'"
        class="w-full max-w-xl rounded-2xl border border-gray-300 px-4 py-3 text-base focus:outline-none focus:ring-2 focus:ring-blue-500 shadow-sm"
      />

      <!-- Phone label -->
      <label
        for="phone-input"
        class="block text-left w-full max-w-xl mt-4 mb-1 font-medium text-gray-700"
      >
        {{ t("contact_info.enter_phone_number") }}
      </label>

      <!-- Phone field with country select -->
      <div class="w-full max-w-xl flex gap-3 items-center">
        <!-- Country dropdown -->
        <div class="relative">
          <select
            v-model="selectedCountry"
            @change="changeCountry($event.target.value)"
            class="appearance-none pl-10 pr-6 py-3 rounded-2xl border border-gray-300 bg-white shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
          >
            <option v-for="c in countries" :key="c.code" :value="c.code">
              {{ c.label }}
            </option>
          </select>
          <!-- Flag overlay inside select -->
          <img
            :src="`/flags/${selectedCountry}.svg`"
            class="w-5 h-5 absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none"
          />
        </div>

        <!-- Phone input -->
        <input
          v-model="phone"
          type="tel"
          class="flex-1 rounded-2xl border border-gray-300 px-4 py-3 text-base focus:outline-none focus:ring-2 focus:ring-blue-500 shadow-sm"
        />
      </div>
    </main>

    <!-- Navigation buttons -->
    <div class="w-full max-w-xl flex justify-between gap-4 mt-6">
      <!-- Back (gray) -->
      <button
        @click="back"
        class="flex-1 rounded-2xl bg-gray-200 py-4 px-6 text-gray-800 text-lg font-semibold shadow hover:bg-gray-300 active:shadow-none transition-all"
      >
        {{ t("contact_info.back") }}
      </button>
      <!-- Forward (blue) -->
      <button
        @click="forward"
        class="flex-1 rounded-2xl bg-blue-600 py-4 px-6 text-white text-lg font-semibold shadow-lg hover:bg-blue-700 active:shadow-none transition-all"
      >
        {{ t("contact_info.next") }}
      </button>
    </div>
  </div>
</template>
