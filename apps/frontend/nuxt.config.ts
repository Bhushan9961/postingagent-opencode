export default defineNuxtConfig({
  devtools: { enabled: true },
  css: ["~/assets/css/main.css"],
  modules: ["@nuxtjs/tailwindcss", "@nuxtjs/color-mode", "@vueuse/nuxt"],
  colorMode: {
    preference: "system",
    fallback: "dark",
    classSuffix: "",
  },
  runtimeConfig: {
    public: {
      apiBaseUrl: process.env.NUXT_PUBLIC_API_BASE_URL || "http://localhost:8000/api/v1",
    },
  },
  nitro: {
    preset: "netlify",
  },
  app: {
    head: {
      title: "AI Marketing OS",
      meta: [{ name: "description", content: "AI Marketing Operating System" }],
    },
  },
})
