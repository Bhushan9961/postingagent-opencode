<template>
  <header class="border-b border-gray-200 bg-white dark:border-gray-700 dark:bg-gray-800">
    <div class="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
      <div class="flex items-center gap-4">
        <NuxtLink to="/" class="text-xl font-bold text-gray-900 dark:text-white">
          AI Marketing OS
        </NuxtLink>
      </div>
      <nav class="flex items-center gap-4">
        <ColorModeToggle />
      </nav>
    </div>
  </header>
</template>
