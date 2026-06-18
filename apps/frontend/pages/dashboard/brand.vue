<template>
  <div class="space-y-6">
    <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Brand Center</h1>
    <div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
      <div class="rounded-xl border bg-white p-6 dark:border-gray-700 dark:bg-gray-800">
        <h2 class="mb-4 text-lg font-semibold text-gray-900 dark:text-white">Colors</h2>
        <div class="flex gap-3">
          <div v-for="c in brandColors" :key="c.name" class="text-center">
            <div class="mb-1 h-12 w-12 rounded-lg shadow" :style="{ backgroundColor: c.hex }" />
            <span class="text-xs text-gray-500 dark:text-gray-400">{{ c.name }}</span>
          </div>
        </div>
      </div>
      <div class="rounded-xl border bg-white p-6 dark:border-gray-700 dark:bg-gray-800">
        <h2 class="mb-4 text-lg font-semibold text-gray-900 dark:text-white">Typography</h2>
        <p class="text-xl font-bold text-gray-900 dark:text-white" style="font-family: Inter">Inter Bold</p>
        <p class="text-base text-gray-700 dark:text-gray-300" style="font-family: Inter">Inter Regular — ABCDEFGHIJKLMNOPQRSTUVWXYZ</p>
      </div>
      <div class="rounded-xl border bg-white p-6 dark:border-gray-700 dark:bg-gray-800">
        <h2 class="mb-4 text-lg font-semibold text-gray-900 dark:text-white">Tone & Voice</h2>
        <ul class="space-y-2 text-sm text-gray-600 dark:text-gray-400">
          <li><strong>Professional</strong> — avoid slang or overly casual language</li>
          <li><strong>Innovative</strong> — position as forward-thinking</li>
          <li><strong>Helpful</strong> — educate, don't just sell</li>
          <li><strong>Confident</strong> — use authoritative language</li>
        </ul>
      </div>
      <div class="rounded-xl border bg-white p-6 dark:border-gray-700 dark:bg-gray-800">
        <h2 class="mb-4 text-lg font-semibold text-gray-900 dark:text-white">Logo</h2>
        <div class="flex h-32 items-center justify-center rounded-lg bg-gray-50 text-gray-400 dark:bg-gray-700">
          Logo placeholder
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const brandColors = [
  { name: "Primary", hex: "#3b82f6" },
  { name: "Secondary", hex: "#1e40af" },
  { name: "Accent", hex: "#06b6d4" },
  { name: "Dark", hex: "#0f172a" },
  { name: "Light", hex: "#f8fafc" },
]
</script>
