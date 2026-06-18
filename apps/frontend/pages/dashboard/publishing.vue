<template>
  <div class="space-y-6">
    <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Publishing Center</h1>
    <div class="rounded-xl border bg-white dark:border-gray-700 dark:bg-gray-800">
      <table class="w-full text-left text-sm">
        <thead class="border-b text-gray-500 dark:border-gray-700 dark:text-gray-400">
          <tr>
            <th class="px-6 py-3 font-medium">Content</th>
            <th class="px-6 py-3 font-medium">Platform</th>
            <th class="px-6 py-3 font-medium">Scheduled</th>
            <th class="px-6 py-3 font-medium">Status</th>
            <th class="px-6 py-3 font-medium">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y dark:divide-gray-700">
          <tr v-for="p in publications" :key="p.id" class="text-gray-700 dark:text-gray-300">
            <td class="px-6 py-3 font-medium">{{ p.title }}</td>
            <td class="px-6 py-3">{{ p.platform }}</td>
            <td class="px-6 py-3">{{ p.scheduled }}</td>
            <td class="px-6 py-3"><StatusBadge :status="p.status" /></td>
            <td class="px-6 py-3">
              <button v-if="p.status === 'pending'" class="text-brand-600 hover:text-brand-700">Publish Now</button>
              <button v-else class="text-gray-400">View</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
const publications = ref([
  { id: 1, title: "AI Tool Demo Video", platform: "YouTube", scheduled: "2026-06-20 10:00", status: "scheduled" },
  { id: 2, title: "Case Study: Client X", platform: "LinkedIn", scheduled: "2026-06-21 09:00", status: "pending" },
  { id: 3, title: "Product Teaser", platform: "Instagram", scheduled: "2026-06-22 12:00", status: "draft" },
  { id: 4, title: "Behind the Scenes", platform: "X", scheduled: "2026-06-23 14:00", status: "published" },
])
</script>
