<!-- =================================================== -->
<!-- EditForm.vue                                         -->
<!-- =================================================== -->

<script setup>
import { computed, ref } from "vue";
import { useI18n } from "vue-i18n";
import { useRouter } from "vue-router";
import { useFlowStore } from "@/store";
import { savePolicyDraft } from "@/services/api";

const { t } = useI18n();
const router = useRouter();
const flow = useFlowStore();

const fields = computed(() => [
  { key: "last_name", label: t("edit_form.fields.last_name") },
  { key: "first_name", label: t("edit_form.fields.first_name") },
  { key: "middle_name", label: t("edit_form.fields.middle_name") },
  { key: "sex", label: t("edit_form.fields.sex") },
  { key: "birthday", label: t("edit_form.fields.birthday"), type: "date" },
  { key: "passport_series", label: t("edit_form.fields.passport_series") },
  { key: "passport_number", label: t("edit_form.fields.passport_number") },
  {
    key: "passport_issue_date",
    label: t("edit_form.fields.passport_issue_date"),
    type: "date",
  },
  {
    key: "passport_expiry_date",
    label: t("edit_form.fields.passport_expiry_date"),
    type: "date",
  },
  { key: "passport_issuer", label: t("edit_form.fields.passport_issuer") },
]);

const submitting = ref(false);

function back() {
  router.back();
}

async function pay() {
  if (submitting.value) return;
  submitting.value = true;

  try {
    if (!flow.employeeTabNumber) {
      throw new Error(
        t("landing.employee_required") || "Введите табельный номер",
      );
    }

    const payload = {
      employee_tab_number: String(flow.employeeTabNumber),
      arrived_for_hire: !!flow.arrived_for_hire,
      lang: flow.lang,
      policy_variant: flow.policyVariant,
      user: { ...flow.formData },
      contacts: { ...flow.formContacts },
      policy: {
        title: flow.formPolicy.title,
        amount: flow.formPolicy.price,
      },
    };

    const response = await savePolicyDraft(payload);
    flow.policyId = response.policy_id;

    router.push("/payment_init");
  } catch (err) {
    console.error("savePolicyDraft failed", err);
    const msg = err && err.message ? err.message : String(err);
    alert(msg || t("edit_form.submit_error") || "Ошибка сохранения данных");
  } finally {
    submitting.value = false;
  }
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
        class="w-60 h-auto my-6 ml-0 select-none pointer-events-none self-start"
      />
      <h1 class="font-extrabold leading-tight text-3xl sm:text-4xl md:text-5xl">
        {{ t("edit_form.title") }}
      </h1>

      <div class="grid gap-4 text-left grid-cols-1 sm:grid-cols-2 w-full">
        <div v-for="f in fields" :key="f.key">
          <label class="block mb-1 font-medium text-sm text-gray-700">{{
            f.label
          }}</label>
          <input
            :value="flow.formData[f.key]"
            @input="flow.formData[f.key] = $event.target.value"
            :type="f.type || 'text'"
            class="w-full rounded-2xl border border-gray-300 px-4 py-3 text-base focus:outline-none focus:ring-2 focus:ring-blue-500 shadow-sm"
          />
        </div>
      </div>
    </main>

    <div class="w-full max-w-xl mt-6">
      <label
        class="flex items-center gap-3 text-base font-medium text-gray-700 cursor-pointer"
      >
        <input
          type="checkbox"
          v-model="flow.arrived_for_hire"
          class="h-5 w-5 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
        />
        {{ t("edit_form.arrived_for_hire") }}
      </label>
    </div>

    <div class="w-full max-w-xl flex justify-between gap-4 mt-6">
      <button
        @click="back"
        class="flex-1 rounded-2xl bg-gray-200 py-4 px-6 text-gray-800 text-lg font-semibold shadow hover:bg-gray-300 active:shadow-none transition-all"
      >
        {{ t("edit_form.back") }}
      </button>
      <button
        @click="pay"
        :disabled="submitting"
        class="flex-1 rounded-2xl bg-blue-600 py-4 px-6 text-white text-lg font-semibold shadow-lg hover:bg-blue-700 active:shadow-none transition-all disabled:opacity-60"
      >
        {{ submitting ? t("edit_form.saving") : t("edit_form.pay") }}
      </button>
    </div>
  </div>
</template>
