import { defineStore } from "pinia"

interface User {
  id: number
  email: string
  full_name: string
  role: string
}

export const useAuthStore = defineStore("auth", () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(null)

  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.role === "admin")
  const isReviewer = computed(() => user.value?.role === "content_reviewer" || user.value?.role === "admin")

  async function login(email: string, password: string) {
    const { $api } = useNuxtApp()
    const res = await $api("/auth/login", {
      method: "POST",
      body: { email, password },
    })
    token.value = res.access_token
    const me = await $api("/auth/me", { headers: { Authorization: `Bearer ${token.value}` } })
    user.value = me
  }

  function logout() {
    user.value = null
    token.value = null
    navigateTo("/login")
  }

  return { user, token, isAuthenticated, isAdmin, isReviewer, login, logout }
})
