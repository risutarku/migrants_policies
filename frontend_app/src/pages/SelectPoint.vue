<template>
  <div class="p-8 max-w-md mx-auto">
    <h2 class="text-xl font-semibold mb-4">{{ $t("Choose point") }}</h2>
    <ul class="space-y-2">
      <li
        v-for="p in points"
        :key="p"
        @click="selectPoint(p)"
        class="border p-3 rounded hover:bg-gray-100 cursor-pointer"
      >
        {{ p }}
      </li>
    </ul>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";
import { useFlowStore } from "../store";

const router = useRouter();
const store = useFlowStore();
const points = ["A-Gate", "B-Gate", "C-Gate"]; // позже заменим API

function selectPoint(p) {
  store.point = p;
  router.push("/scan");
}
</script>
