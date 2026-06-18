<template>
  <span
    class="inline-block rounded-full px-2.5 py-0.5 text-xs font-medium"
    :class="{
      'bg-green-100 text-green-700 dark:bg-green-900/20 dark:text-green-400': status === 'active' || status === 'published' || status === 'completed',
      'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/20 dark:text-yellow-400': status === 'pending' || status === 'scheduled' || status === 'running',
      'bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-400': status === 'draft' || status === 'idle',
      'bg-red-100 text-red-700 dark:bg-red-900/20 dark:text-red-400': status === 'failed',
    }"
  >
    {{ status }}
  </span>
</template>

<script setup lang="ts">
defineProps<{ status: string }>()
</script>
