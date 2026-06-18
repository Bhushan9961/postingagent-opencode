<template>
  <div class="space-y-6">
    <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Platform Rules</h1>
    <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
      <div v-for="(rules, platform) in platformRules" :key="platform" class="rounded-xl border bg-white p-4 dark:border-gray-700 dark:bg-gray-800">
        <h3 class="mb-2 text-lg font-semibold capitalize text-gray-900 dark:text-white">{{ platform }}</h3>
        <ul class="space-y-1 text-sm text-gray-600 dark:text-gray-400">
          <li v-for="(v, k) in rules" :key="k">
            <span class="font-medium text-gray-700 dark:text-gray-300">{{ k }}:</span> {{ v }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const platformRules = {
  linkedin: { caption_limit: "3,000 chars", video_max: "10 min", carousel_max: "10 pages" },
  instagram: { caption_limit: "2,200 chars", video_max: "90 sec", carousel_max: "10 pages" },
  facebook: { caption_limit: "63,206 chars", video_max: "240 min", image_size: "1200x630" },
  x: { caption_limit: "280 chars", video_max: "140 sec", image_size: "1600x1600" },
  youtube: { thumbnail: "1280x720", video_max: "12 hours", shorts_max: "60 sec" },
  pinterest: { caption_limit: "500 chars", image_ratio: "2:3", video_max: "15 min" },
}
</script>
