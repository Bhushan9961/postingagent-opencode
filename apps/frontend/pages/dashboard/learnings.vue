<template>
  <div class="space-y-6">
    <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Learnings</h1>
    <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
      <div v-for="l in learnings" :key="l.title" class="rounded-xl border bg-white p-4 dark:border-gray-700 dark:bg-gray-800">
        <div class="mb-2 inline-block rounded bg-green-100 px-2 py-0.5 text-xs font-medium text-green-700 dark:bg-green-900/20 dark:text-green-400">
          {{ l.tag }}
        </div>
        <h3 class="font-medium text-gray-900 dark:text-white">{{ l.title }}</h3>
        <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">{{ l.description }}</p>
        <div class="mt-2 flex items-center gap-2">
          <span class="text-xs text-gray-400">Win rate: {{ l.winRate }}%</span>
          <span class="text-xs text-gray-400">•</span>
          <span class="text-xs text-gray-400">{{ l.samples }} samples</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const learnings = ref([
  { title: "Question hooks outperform stat hooks", tag: "Hook", description: "When starting with a question, CTR improves 35% vs statistics-based hooks on LinkedIn.", winRate: 78, samples: 45 },
  { title: "Best posting time: 9-11 AM EST", tag: "Timing", description: "Posts published between 9-11 AM EST get 2.3x more engagement across all platforms.", winRate: 92, samples: 120 },
  { title: "Carousel: 5 slides optimal", tag: "Format", description: "LinkedIn carousels with exactly 5 slides have the highest completion rate.", winRate: 85, samples: 67 },
  { title: "Emotional CTAs convert 2.1x better", tag: "CTA", description: "CTAs that evoke urgency or curiosity outperform generic 'Learn More' by 2.1x.", winRate: 74, samples: 89 },
  { title: "Video length: 30-45s sweet spot", tag: "Video", description: "Short-form videos between 30-45 seconds have highest retention and CTR.", winRate: 88, samples: 56 },
  { title: "Case studies drive 3x more leads", tag: "Content", description: "Case study content converts 3x better than product-focused content for B2B.", winRate: 91, samples: 34 },
])
</script>
