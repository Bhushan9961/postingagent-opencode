<template>
  <div class="rounded-xl border bg-white p-4 dark:border-gray-700 dark:bg-gray-800">
    <div class="flex items-center justify-between">
      <h3 class="font-medium text-gray-900 dark:text-white">{{ name }}</h3>
      <StatusBadge :status="status" />
    </div>
    <div class="mt-2 flex items-center justify-between text-sm text-gray-500 dark:text-gray-400">
      <span>Last run: {{ lastRun }}</span>
      <span>Score: {{ score }}%</span>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{ name: string; status: string; lastRun: string; score: number }>()
</script>
