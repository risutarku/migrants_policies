<!-- =================================================== -->
<!-- ScanDocument.vue                                     -->
<!-- =================================================== -->

<script setup>
import { ref } from "vue";
import { useI18n } from "vue-i18n";
import { useRouter } from "vue-router";
import { useFlowStore } from "@/store";
import { scanPassportBeorg } from "@/services/api";
import { fileToBase64NoPrefix } from "@/utils/fileToBase64";

const { t } = useI18n();
const router = useRouter();
const flow = useFlowStore();

const scanning = ref(false);
const overlayVisible = ref(false);
const errorMsg = ref("");
const withRegistration = ref(true);
const stageText = ref("");
let stageTimer = null;

function startProgressText() {
  const stages = [
    "Загружаем изображение…",
    "Отправляем в сервис распознавания…",
    "Распознаём данные…",
    "Проверяем результат…",
    "Почти готово…",
  ];
  let i = 0;
  stageText.value = stages[0];
  stageTimer = setInterval(() => {
    i = Math.min(i + 1, stages.length - 1);
    stageText.value = stages[i];
  }, 2500);
}

function stopProgressText() {
  if (stageTimer) clearInterval(stageTimer);
  stageTimer = null;
  stageText.value = "";
}

// если нужно привести дату DD.MM.YYYY -> YYYY-MM-DD для <input type="date">
function toISODateMaybe(s) {
  if (!s) return s;
  // уже ISO?
  if (/^\d{4}-\d{2}-\d{2}$/.test(s)) return s;

  // DD.MM.YYYY
  const m = String(s).match(/^(\d{2})\.(\d{2})\.(\d{4})$/);
  if (m) return `${m[3]}-${m[2]}-${m[1]}`;

  return s;
}

function back() {
  router.back();
}

function startOverlay() {
  overlayVisible.value = true;
  scanning.value = true;
  startProgressText();
}

function stopOverlay() {
  scanning.value = false;
  stopProgressText();
  overlayVisible.value = false;
}

async function onFilesSelected(e) {
  errorMsg.value = "";
  const files = Array.from(e.target.files || []);
  if (!files.length) return;

  startOverlay();

  try {
    // 1) файл(ы) -> base64[]
    const images = [];
    for (const f of files) {
      images.push(await fileToBase64NoPrefix(f));
    }

    // 2) отправляем на бэк
    const res = await scanPassportBeorg(images, withRegistration.value);
    const fields = res?.fields || {};

    // 3) маппинг в твою форму
    if (fields.last_name) flow.formData.last_name = fields.last_name;
    if (fields.first_name) flow.formData.first_name = fields.first_name;
    if (fields.middle_name) flow.formData.middle_name = fields.middle_name;

    if (fields.sex) flow.formData.sex = fields.sex;

    if (fields.birthday)
      flow.formData.birthday = toISODateMaybe(fields.birthday);

    if (fields.passport_series)
      flow.formData.passport_series = fields.passport_series;
    if (fields.passport_number)
      flow.formData.passport_number = fields.passport_number;

    if (fields.passport_issue_date)
      flow.formData.passport_issue_date = toISODateMaybe(
        fields.passport_issue_date,
      );

    if (fields.passport_issuer)
      flow.formData.passport_issuer = fields.passport_issuer;

    // 4) переход на редактирование
    router.push("/edit");
  } catch (err) {
    console.error(err);
    errorMsg.value = err?.message ? String(err.message) : String(err);
  } finally {
    stopOverlay();
    // чтобы можно было выбрать тот же файл ещё раз
    e.target.value = "";
  }
}
</script>

<template>
  <div
    class="relative flex flex-col items-center min-h-screen bg-gradient-to-b from-sky-50 to-white px-4 py-8 overflow-hidden"
  >
    <main
      class="flex flex-col items-center justify-center text-center space-y-8 max-w-2xl flex-1 w-full"
    >
      <img
        src="/logo_ing.svg"
        alt="Ingosstrakh logo"
        class="w-60 h-auto my-6 ml-14 select-none pointer-events-none self-start"
      />

      <h1
        class="font-extrabold leading-tight text-3xl sm:text-4xl md:text-5xl whitespace-pre-line"
      >
        {{ t("scan_document.title") }}
      </h1>

      <img
        src="/scan_document.png"
        alt="scan"
        class="w-120 h-auto pointer-events-none select-none"
        loading="eager"
      />

      <!-- NEW: выбор файлов паспорта -->
      <div class="w-full max-w-md text-left space-y-3">
        <input
          type="file"
          accept="image/*"
          multiple
          @change="onFilesSelected"
          :disabled="scanning"
          class="block w-full text-sm text-gray-700 file:mr-4 file:py-3 file:px-4 file:rounded-2xl file:border-0 file:text-sm file:font-semibold file:bg-blue-600 file:text-white hover:file:bg-blue-700"
        />

        <p class="text-sm text-gray-600">
          Можно выбрать 1–2 изображения (разворот + прописка).
        </p>

        <div
          v-if="errorMsg"
          class="rounded-2xl bg-red-50 border border-red-200 p-3 text-red-700"
        >
          {{ errorMsg }}
        </div>
      </div>
    </main>

    <!-- Scanning stripe overlay -->
    <!-- <div
      v-if="overlayVisible"
      class="absolute inset-0 pointer-events-none overflow-hidden"
    >
      <div
        class="absolute top-0 left-0 w-full h-2 bg-blue-500 animate-scan-strip"
      ></div>
    </div> -->

    <div
      v-if="overlayVisible"
      class="absolute inset-0 bg-white/70 backdrop-blur-sm flex flex-col items-center justify-center z-50"
    >
      <div
        class="h-10 w-10 rounded-full border-4 border-gray-300 border-t-blue-600 animate-spin"
      ></div>
      <div class="mt-4 text-lg font-semibold text-gray-800">
        {{ stageText || "Распознаём документ…" }}
      </div>
      <div class="mt-2 text-sm text-gray-600">
        Обычно занимает 5–15 секунд. Пожалуйста, не закрывайте страницу.
      </div>
    </div>

    <div class="w-full flex flex-col items-center gap-3">
      <button
        @click="back"
        class="w-full max-w-xs rounded-2xl bg-gray-200 py-4 px-6 text-gray-800 text-lg font-semibold shadow hover:bg-gray-300 active:shadow-none transition-all"
        :disabled="scanning"
      >
        {{ t("scan_document.back") }}
      </button>
    </div>
  </div>
</template>

<style scoped>
@keyframes scan {
  0% {
    transform: translateY(-100%);
  }
  100% {
    transform: translateY(100vh);
  }
}

.animate-scan-strip {
  animation: scan 1.5s linear forwards;
}
</style>
