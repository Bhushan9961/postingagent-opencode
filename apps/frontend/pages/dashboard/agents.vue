<template>
  <div class="space-y-6">
    <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Agent Monitor</h1>
    <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
      <AgentCard v-for="agent in agents" :key="agent.name" v-bind="agent" />
    </div>
  </div>
</template>

<script setup lang="ts">
const agents = [
  { name: "Research Agent", status: "idle", lastRun: "2m ago", score: 98 },
  { name: "Strategy Agent", status: "running", lastRun: "now", score: 92 },
  { name: "Storytelling Agent", status: "completed", lastRun: "5m ago", score: 95 },
  { name: "Quality Control", status: "idle", lastRun: "10m ago", score: 88 },
  { name: "Publisher Agent", status: "waiting", lastRun: "15m ago", score: 100 },
  { name: "Analytics Agent", status: "running", lastRun: "now", score: 90 },
  { name: "Learning Agent", status: "idle", lastRun: "1h ago", score: 85 },
  { name: "Image Agent", status: "completed", lastRun: "3m ago", score: 94 },
]
</script>
