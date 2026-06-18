<template>
  <div v-if="!isAuthPage" class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <AppSidebar />
    <div class="pl-64">
      <header class="flex h-16 items-center justify-end border-b border-gray-200 bg-white px-6 dark:border-gray-700 dark:bg-gray-800">
        <ColorModeToggle />
      </header>
      <main class="p-6">
        <slot />
      </main>
    </div>
  </div>
  <div v-else>
    <slot />
  </div>
</template>

<script setup lang="ts">
const route = useRoute()
const isAuthPage = computed(() => route.path === "/login")
</script>
