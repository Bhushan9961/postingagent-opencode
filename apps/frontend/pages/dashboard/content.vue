<template>
  <div class="space-y-6">
    <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Content Library</h1>
    <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
      <div v-for="i in 6" :key="i" class="rounded-xl border bg-white p-4 dark:border-gray-700 dark:bg-gray-800">
        <div class="mb-3 aspect-video rounded-lg bg-gray-100 dark:bg-gray-700" />
        <h3 class="font-medium text-gray-900 dark:text-white">Content {{ i }}</h3>
        <p class="text-sm text-gray-500 dark:text-gray-400">LinkedIn • Carousel</p>
      </div>
    </div>
  </div>
</template>
