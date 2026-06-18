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
    try {
      const { $api } = useNuxtApp()
      const res = await $api("/auth/login", {
        method: "POST",
        body: { email, password },
      })
      token.value = res.access_token
      localStorage.setItem("auth_token", res.access_token)
      const me = await $api("/auth/me", { headers: { Authorization: `Bearer ${token.value}` } })
      user.value = me
    } catch (error) {
      token.value = null
      user.value = null
      localStorage.removeItem("auth_token")
      throw error
    }
  }

  function logout() {
    user.value = null
    token.value = null
    localStorage.removeItem("auth_token")
  }

  function initialize() {
    const savedToken = localStorage.getItem("auth_token")
    if (savedToken) {
      token.value = savedToken
    }
  }

  initialize()

  return { user, token, isAuthenticated, isAdmin, isReviewer, login, logout }
})
