<template>
  <div class="rounded-xl border bg-white p-6 dark:border-gray-700 dark:bg-gray-800">
    <p class="text-sm font-medium text-gray-500 dark:text-gray-400">{{ title }}</p>
    <p class="mt-2 text-3xl font-bold text-gray-900 dark:text-white">{{ value }}</p>
    <p v-if="change" class="mt-1 text-sm" :class="change.startsWith('+') ? 'text-green-600' : 'text-red-600'">
      {{ change }} from last month
    </p>
  </div>
</template>

<script setup lang="ts">
defineProps<{ title: string; value: string; change?: string }>()
</script>
