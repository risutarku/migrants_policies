<!-- <script setup lang="ts">
import { useI18n } from "vue-i18n";
import { useRouter } from "vue-router";
import { useFlowStore } from "@/store";
import { getPolicyQuote, downloadPolicyXlsxFromQuote } from "@/services/api";

const { t } = useI18n();
const router = useRouter();
const flow = useFlowStore();

async function downloadPolicy() {
  const quote = await getPolicyQuote({
    user: flow.formData,
    inputs: {
      employee_tab_number: flow.employeeTabNumber,
      arrived_for_hire: flow.arrived_for_hire,
      start_date: flow.startDate, // если есть
      end_date: flow.endDate, // если есть
      base_premium: flow.formPolicy.price,
      seq: 1,
    },
  });

  flow.policyQuote = quote;

  const blob = await downloadPolicyXlsxFromQuote(quote);

  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `${quote.policy_number}.xlsx`;
  a.click();
  URL.revokeObjectURL(url);
}

function done() {
  // очищаем стор или переходим на главную
  flow.$reset?.(); // если Pinia v2, иначе вручную
  router.push("/");
}
</script>

<template>
  <div
    class="flex flex-col items-center min-h-screen bg-gradient-to-b from-sky-50 to-white px-4 py-8"
  >
    <main
      class="flex flex-col items-center justify-center text-center space-y-6 max-w-xl flex-1 w-full"
    >
      <img
        src="/logo_ing.svg"
        alt="Ingosstrakh logo"
        class="w-60 h-auto my-6 ml-22 select-none pointer-events-none self-start"
      />
      <h1 class="font-extrabold leading-tight text-3xl sm:text-4xl md:text-5xl">
        {{ t("payment_success.title") }}
      </h1>
      <p class="text-lg text-gray-700 max-w-md">
        {{ t("payment_success.text_1") }}
        {{ flow.formContacts.email }}
      </p>
      <p class="text-lg text-gray-700 max-w-md">
        {{ t("payment_success.text_2") }}
      </p>
    </main>

    <button
      @click="done"
      class="w-full max-w-xs rounded-2xl bg-blue-600 py-4 px-6 text-white text-lg font-semibold shadow-lg hover:bg-blue-700 active:shadow-none transition-all"
    >
      {{ t("payment_success.done") }}
    </button>
  </div>
</template> -->
<script setup lang="ts">
import { ref } from "vue";
import { useI18n } from "vue-i18n";
import { useRouter } from "vue-router";
import { useFlowStore } from "@/store";
import { getPolicyQuote, downloadPolicyXlsxFromQuote } from "@/services/api";

const { t } = useI18n();
const router = useRouter();
const flow = useFlowStore();

const generating = ref(false);

async function generateAndDownloadPolicy() {
  if (generating.value) return;
  generating.value = true;

  try {
    // 1) Собираем данные из store (они уже заполнены на EditForm)
    const payload = {
      user: flow.formData,
      inputs: {
        employee_tab_number: flow.employeeTabNumber,
        arrived_for_hire: flow.arrived_for_hire,
        base_premium: flow.formPolicy.price,
        // если появятся даты в UI — передашь сюда:
        // start_date: flow.startDate,
        // end_date: flow.endDate,
        seq: 1, // временно, пока без БД
      },
    };

    // 2) Запрос расчёта у бэка
    const quote = await getPolicyQuote(payload);
    flow.policyQuote = quote;

    // 3) Генерация Excel по готовому quote
    const blob = await downloadPolicyXlsxFromQuote(quote);

    // 4) Скачивание файла
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${quote.policy_number || "policy"}.xlsx`;
    a.click();
    URL.revokeObjectURL(url);
  } catch (e: any) {
    console.error(e);
    alert(e?.message || "Ошибка генерации полиса");
  } finally {
    generating.value = false;
  }
}

function done() {
  // ВАЖНО: не сбрасывай store до того, как скачал полис
  flow.$reset?.();
  router.push("/");
}
</script>

<template>
  <div
    class="flex flex-col items-center min-h-screen bg-gradient-to-b from-sky-50 to-white px-4 py-8"
  >
    <main
      class="flex flex-col items-center justify-center text-center space-y-6 max-w-xl flex-1 w-full"
    >
      <img
        src="/logo_ing.svg"
        alt="Ingosstrakh logo"
        class="w-60 h-auto my-6 ml-22 select-none pointer-events-none self-start"
      />
      <h1 class="font-extrabold leading-tight text-3xl sm:text-4xl md:text-5xl">
        {{ t("payment_success.title") }}
      </h1>

      <p class="text-lg text-gray-700 max-w-md">
        {{ t("payment_success.text_1") }}
        {{ flow.formContacts.email }}
      </p>
      <p class="text-lg text-gray-700 max-w-md">
        {{ t("payment_success.text_2") }}
      </p>

      <!-- НОВАЯ КНОПКА: скачать полис -->
      <button
        @click="generateAndDownloadPolicy"
        :disabled="generating"
        class="w-full max-w-xs rounded-2xl bg-white border-2 border-gray-300 py-4 px-6 text-gray-900 text-lg font-semibold shadow hover:bg-gray-50 active:shadow-none transition-all disabled:opacity-60"
      >
        {{ generating ? "Генерирую..." : "Скачать полис (Excel)" }}
      </button>
    </main>

    <button
      @click="done"
      class="w-full max-w-xs rounded-2xl bg-blue-600 py-4 px-6 text-white text-lg font-semibold shadow-lg hover:bg-blue-700 active:shadow-none transition-all"
    >
      {{ t("payment_success.done") }}
    </button>
  </div>
</template>
