<template>
  <div class="space-y-6">
    <h1 class="text-2xl font-bold text-gray-900 dark:text-white">A/B Testing</h1>
    <div class="grid grid-cols-1 gap-6 sm:grid-cols-2">
      <div v-for="test in abTests" :key="test.name" class="rounded-xl border bg-white p-6 dark:border-gray-700 dark:bg-gray-800">
        <h3 class="font-semibold text-gray-900 dark:text-white">{{ test.name }}</h3>
        <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">{{ test.platform }}</p>
        <div class="mt-4 space-y-2 text-sm">
          <p class="text-gray-600 dark:text-gray-400">A: {{ test.variantA }} — <span class="text-green-600">{{ test.winnerA }}</span></p>
          <p class="text-gray-600 dark:text-gray-400">B: {{ test.variantB }} — <span class="text-red-600">{{ test.winnerB }}</span></p>
        </div>
        <div class="mt-2 h-2 rounded-full bg-gray-100 dark:bg-gray-700">
          <div class="h-full rounded-full bg-brand-500" :style="{ width: test.confidence + '%' }" />
        </div>
        <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">{{ test.confidence }}% confidence</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const abTests = ref([
  { name: "Hook Style: Question vs Stat", platform: "LinkedIn", variantA: "Question Hook", winnerA: "4.2% CTR", variantB: "Stat Hook", winnerB: "3.1% CTR", confidence: 95 },
  { name: "Thumbnail: Product vs Person", platform: "YouTube", variantA: "Product Shot", winnerA: "8.9% CTR", variantB: "Person Face", winnerB: "6.2% CTR", confidence: 98 },
  { name: "CTA: Free vs Limited", platform: "Instagram", variantA: "Get Free Guide", winnerA: "2.1% Conv", variantB: "Limited Offer", winnerB: "1.8% Conv", confidence: 78 },
])
</script>
