<template>
  <div class="space-y-6">
    <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Approval Queue</h1>
    <div v-if="pendingItems.length === 0" class="rounded-xl border bg-white p-12 text-center dark:border-gray-700 dark:bg-gray-800">
      <p class="text-gray-500 dark:text-gray-400">No items pending approval.</p>
    </div>
    <div v-else class="space-y-4">
      <div v-for="item in pendingItems" :key="item.id" class="rounded-xl border bg-white p-4 dark:border-gray-700 dark:bg-gray-800">
        <div class="flex items-start justify-between">
          <div>
            <h3 class="font-medium text-gray-900 dark:text-white">{{ item.title }}</h3>
            <p class="text-sm text-gray-500 dark:text-gray-400">{{ item.platform }} • {{ item.type }}</p>
          </div>
          <div class="flex gap-2">
            <button class="rounded-lg bg-green-600 px-4 py-1.5 text-sm text-white hover:bg-green-700" @click="approve(item.id)">Approve</button>
            <button class="rounded-lg bg-red-600 px-4 py-1.5 text-sm text-white hover:bg-red-700" @click="reject(item.id)">Reject</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const pendingItems = ref([
  { id: 1, title: "AI Tool Launch — LinkedIn Carousel", platform: "LinkedIn", type: "carousel" },
  { id: 2, title: "Case Study Teaser — Instagram Reel", platform: "Instagram", type: "video" },
  { id: 3, title: "Product Demo — YouTube Video", platform: "YouTube", type: "video" },
])

function approve(id: number) { pendingItems.value = pendingItems.value.filter(i => i.id !== id) }
function reject(id: number) { pendingItems.value = pendingItems.value.filter(i => i.id !== id) }
</script>
