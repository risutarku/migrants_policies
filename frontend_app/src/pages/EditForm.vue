<!-- EditForm.vue                                         -->
<!-- =================================================== -->

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import { useFlowStore } from '@/store'

const { t } = useI18n()
const router = useRouter()
const flow = useFlowStore()

// Описание полей и подписей
const fields = [
    { key: 'name', label: t('edit_form.fields.name') },
    { key: 'last_name', label: t('edit_form.fields.last_name') },
    { key: 'middle_name', label: t('edit_form.fields.middle_name') },
    { key: 'sex', label: t('edit_form.fields.sex') },
    { key: 'birthday', label: t('edit_form.fields.birthday') },
    { key: 'passport_series', label: t('edit_form.fields.passport_series') },
    { key: 'passport_number', label: t('edit_form.fields.passport_number') },
    { key: 'passport_issue_date', label: t('edit_form.fields.passport_issue_date') },
    { key: 'passport_expiry_date', label: t('edit_form.fields.passport_expiry_date') },
    { key: 'passport_issuer', label: t('edit_form.fields.passport_issuer') },
]

function back() {
    router.back()
}
function pay() {
    router.push('/payment_init')
}
</script>

<template>
    <div class="flex flex-col items-center min-h-screen bg-gradient-to-b from-sky-50 to-white px-4 py-8">
        <main class="flex flex-col items-center justify-center text-center space-y-6 max-w-xl flex-1 w-full">
            <img src="/logo_ing.svg" alt="Ingosstrakh logo"
                class="w-60 h-auto my-6 ml-0 select-none pointer-events-none self-start" />
            <h1 class="font-extrabold leading-tight text-3xl sm:text-4xl md:text-5xl">
                {{ t('edit_form.title') }}
            </h1>

            <!-- Сетка полей (динамический v-bind/value) -->
            <div class="grid gap-4 text-left
            grid-cols-1 sm:grid-cols-2">
                <div v-for="f in fields" :key="f.key">
                    <label class="block mb-1 font-medium text-sm text-gray-700">{{ f.label }}</label>
                    <input :value="flow.formData[f.key]" @input="flow.formData[f.key] = $event.target.value" :type="['birthday', 'passport_issue_date', 'passport_expiry_date']
                        .includes(f.key) ? 'date' : 'text'"
                        class="w-full rounded-2xl border border-gray-300 px-4 py-3 text-base focus:outline-none focus:ring-2 focus:ring-blue-500 shadow-sm" />
                </div>
            </div>
        </main>

        <!-- Кнопки навигации -->
        <div class="w-full max-w-xl flex justify-between gap-4 mt-6">
            <button @click="back"
                class="flex-1 rounded-2xl bg-gray-200 py-4 px-6 text-gray-800 text-lg font-semibold shadow hover:bg-gray-300 active:shadow-none transition-all">
                {{ t('edit_form.back') }}
            </button>
            <button @click="pay"
                class="flex-1 rounded-2xl bg-blue-600 py-4 px-6 text-white text-lg font-semibold shadow-lg hover:bg-blue-700 active:shadow-none transition-all">
                {{ t('edit_form.pay') }}
            </button>
        </div>
    </div>
</template>