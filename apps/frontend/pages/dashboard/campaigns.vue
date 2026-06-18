<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Campaign Management</h1>
      <button class="rounded-lg bg-brand-600 px-4 py-2 text-sm font-medium text-white hover:bg-brand-700">
        + New Campaign
      </button>
    </div>
    <div class="rounded-xl border bg-white dark:border-gray-700 dark:bg-gray-800">
      <table class="w-full text-left text-sm">
        <thead class="border-b text-gray-500 dark:border-gray-700 dark:text-gray-400">
          <tr>
            <th class="px-6 py-3 font-medium">Name</th>
            <th class="px-6 py-3 font-medium">Status</th>
            <th class="px-6 py-3 font-medium">Created</th>
            <th class="px-6 py-3 font-medium">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y dark:divide-gray-700">
          <tr v-for="c in campaigns" :key="c.id" class="text-gray-700 dark:text-gray-300">
            <td class="px-6 py-4 font-medium">{{ c.name }}</td>
            <td class="px-6 py-4"><StatusBadge :status="c.status" /></td>
            <td class="px-6 py-4">{{ c.created_at }}</td>
            <td class="px-6 py-4">
              <button class="text-brand-600 hover:text-brand-700">Edit</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
const campaigns = ref([
  { id: 1, name: "AI Tool Launch Q3", status: "active", created_at: "2026-06-01" },
  { id: 2, name: "Consultancy Brand Awareness", status: "draft", created_at: "2026-06-10" },
  { id: 3, name: "Product Hunt Launch", status: "completed", created_at: "2026-05-15" },
])
</script>
