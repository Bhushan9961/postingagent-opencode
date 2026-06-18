<template>
  <div class="flex min-h-screen items-center justify-center bg-gray-50 px-4 dark:bg-gray-900">
    <div class="w-full max-w-sm space-y-6">
      <div class="text-center">
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">AI Marketing OS</h1>
        <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">Sign in to your account</p>
      </div>
      <div class="rounded-xl border bg-white p-6 shadow-sm dark:border-gray-700 dark:bg-gray-800">
        <form @submit.prevent="handleLogin" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Email</label>
            <input
              v-model="email" type="email" required
              class="mt-1 block w-full rounded-lg border bg-white px-3 py-2 text-sm text-gray-900 placeholder-gray-400 dark:border-gray-600 dark:bg-gray-700 dark:text-white"
              placeholder="you@example.com"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Password</label>
            <input
              v-model="password" type="password" required
              class="mt-1 block w-full rounded-lg border bg-white px-3 py-2 text-sm text-gray-900 placeholder-gray-400 dark:border-gray-600 dark:bg-gray-700 dark:text-white"
              placeholder="••••••••"
            />
          </div>
          <button
            type="submit"
            class="w-full rounded-lg bg-brand-600 px-4 py-2 text-sm font-medium text-white hover:bg-brand-700"
          >
            Sign In
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const email = ref("")
const password = ref("")
const router = useRouter()

async function handleLogin() {
  await navigateTo("/dashboard")
}
</script>
