<template>
  <div class="space-y-6">
    <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Analytics</h1>
    <div class="grid grid-cols-1 gap-6 sm:grid-cols-2">
      <div class="rounded-xl border bg-white p-6 dark:border-gray-700 dark:bg-gray-800">
        <h2 class="mb-4 text-lg font-semibold text-gray-900 dark:text-white">Views Over Time</h2>
        <div class="h-64 rounded-lg bg-gray-50 dark:bg-gray-700" />
      </div>
      <div class="rounded-xl border bg-white p-6 dark:border-gray-700 dark:bg-gray-800">
        <h2 class="mb-4 text-lg font-semibold text-gray-900 dark:text-white">Engagement Rate</h2>
        <div class="h-64 rounded-lg bg-gray-50 dark:bg-gray-700" />
      </div>
    </div>
    <div class="rounded-xl border bg-white dark:border-gray-700 dark:bg-gray-800">
      <table class="w-full text-left text-sm">
        <thead class="border-b text-gray-500 dark:border-gray-700 dark:text-gray-400">
          <tr>
            <th class="px-6 py-3 font-medium">Content</th>
            <th class="px-6 py-3 font-medium">Views</th>
            <th class="px-6 py-3 font-medium">Likes</th>
            <th class="px-6 py-3 font-medium">Shares</th>
            <th class="px-6 py-3 font-medium">CTR</th>
          </tr>
        </thead>
        <tbody class="divide-y dark:divide-gray-700">
          <tr v-for="row in metrics" :key="row.name" class="text-gray-700 dark:text-gray-300">
            <td class="px-6 py-3">{{ row.name }}</td>
            <td class="px-6 py-3">{{ row.views }}</td>
            <td class="px-6 py-3">{{ row.likes }}</td>
            <td class="px-6 py-3">{{ row.shares }}</td>
            <td class="px-6 py-3">{{ row.ctr }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
const metrics = ref([
  { name: "AI Tool Demo Video", views: "12.4K", likes: "892", shares: "234", ctr: "4.2%" },
  { name: "Case Study: Client X", views: "8.1K", likes: "445", shares: "123", ctr: "3.8%" },
  { name: "Product Teaser", views: "5.3K", likes: "312", shares: "89", ctr: "2.9%" },
])
</script>
