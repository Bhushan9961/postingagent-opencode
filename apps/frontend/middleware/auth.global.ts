import { useAuthStore } from "~/stores/auth"

export default defineNuxtRouteMiddleware((to) => {
  if (!to.path.startsWith("/dashboard")) {
    return
  }
  const authStore = useAuthStore()
  if (!authStore.isAuthenticated) {
    return navigateTo("/login")
  }
})
