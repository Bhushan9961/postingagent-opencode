<template>
  <button
    class="rounded-lg p-2 text-gray-500 hover:bg-gray-100 dark:text-gray-400 dark:hover:bg-gray-700"
    @click="toggleColorMode"
  >
    <Icon v-if="colorMode === 'dark'" name="heroicons:sun" class="h-5 w-5" />
    <Icon v-else name="heroicons:moon" class="h-5 w-5" />
  </button>
</template>

<script setup lang="ts">
const colorMode = useColorMode()

function toggleColorMode() {
  colorMode.preference = colorMode.value === "dark" ? "light" : "dark"
}
</script>
