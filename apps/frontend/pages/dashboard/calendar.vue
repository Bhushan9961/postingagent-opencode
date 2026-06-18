<template>
  <div class="space-y-6">
    <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Content Calendar</h1>
    <div class="rounded-xl border bg-white dark:border-gray-700 dark:bg-gray-800">
      <div class="grid grid-cols-7 border-b text-center text-sm font-medium text-gray-500 dark:border-gray-700 dark:text-gray-400">
        <div v-for="day in ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']" :key="day" class="border-r py-3 last:border-r-0 dark:border-gray-700">
          {{ day }}
        </div>
      </div>
      <div class="grid grid-cols-7">
        <div v-for="i in 30" :key="i" class="min-h-24 border-b border-r p-2 text-sm dark:border-gray-700"
          :class="{ 'bg-brand-50 dark:bg-brand-900/20': i === 15 }">
          <span class="font-medium text-gray-700 dark:text-gray-300">{{ i }}</span>
        </div>
      </div>
    </div>
  </div>
</template>
