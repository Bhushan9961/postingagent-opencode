<template>
  <aside class="fixed left-0 top-0 z-40 h-full w-64 border-r border-gray-200 bg-white dark:border-gray-700 dark:bg-gray-800">
    <div class="flex h-16 items-center border-b border-gray-200 px-6 dark:border-gray-700">
      <NuxtLink to="/" class="text-lg font-bold text-gray-900 dark:text-white">
        AI Marketing OS
      </NuxtLink>
    </div>
    <nav class="space-y-1 px-3 py-4">
      <NuxtLink
        v-for="item in navItems"
        :key="item.to"
        :to="item.to"
        class="flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors"
        :class="isActive(item.to)
          ? 'bg-brand-50 text-brand-700 dark:bg-brand-900/20 dark:text-brand-400'
          : 'text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700'"
      >
        <span class="text-lg">{{ item.icon }}</span>
        {{ item.label }}
      </NuxtLink>
    </nav>
    <div class="absolute bottom-0 left-0 right-0 border-t border-gray-200 p-4 dark:border-gray-700">
      <button
        class="flex w-full items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700"
        @click="logout"
      >
        <span class="text-lg">→</span>
        Sign Out
      </button>
    </div>
  </aside>
</template>

<script setup lang="ts">
const route = useRoute()
const { logout } = useAuth()

const navItems = [
  { label: "Executive Overview", to: "/dashboard", icon: "◉" },
  { label: "Campaign Management", to: "/dashboard/campaigns", icon: "⚡" },
  { label: "Content Library", to: "/dashboard/content", icon: "▣" },
  { label: "Agent Monitor", to: "/dashboard/agents", icon: "⚙" },
  { label: "Content Calendar", to: "/dashboard/calendar", icon: "☰" },
  { label: "Platform Rules", to: "/dashboard/platform-rules", icon: "☷" },
  { label: "Analytics", to: "/dashboard/analytics", icon: "◈" },
  { label: "A/B Testing", to: "/dashboard/ab-testing", icon: "⇄" },
  { label: "Learnings", to: "/dashboard/learnings", icon: "◎" },
  { label: "Brand Center", to: "/dashboard/brand", icon: "◐" },
  { label: "Approval Queue", to: "/dashboard/approvals", icon: "☑" },
  { label: "Publishing Center", to: "/dashboard/publishing", icon: "↗" },
]

function isActive(to: string) {
  return route.path === to || route.path.startsWith(to + "/")
}
</script>
