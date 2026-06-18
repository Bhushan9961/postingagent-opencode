<template>
  <div class="space-y-6">
    <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Executive Overview</h1>
    <div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
      <StatCard title="Active Campaigns" value="3" change="+1" />
      <StatCard title="Content Published" value="47" change="+12" />
      <StatCard title="Total Reach" value="84.2K" change="+23%" />
      <StatCard title="Avg. Engagement" value="4.8%" change="+0.6%" />
    </div>
    <div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
      <div class="rounded-xl border bg-white p-6 dark:border-gray-700 dark:bg-gray-800">
        <h2 class="mb-4 text-lg font-semibold text-gray-900 dark:text-white">Campaign Performance</h2>
        <p class="text-gray-500 dark:text-gray-400">Chart placeholder</p>
      </div>
      <div class="rounded-xl border bg-white p-6 dark:border-gray-700 dark:bg-gray-800">
        <h2 class="mb-4 text-lg font-semibold text-gray-900 dark:text-white">Platform Distribution</h2>
        <p class="text-gray-500 dark:text-gray-400">Chart placeholder</p>
      </div>
    </div>
  </div>
</template>
