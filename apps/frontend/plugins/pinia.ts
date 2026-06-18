import { createPinia } from "pinia"

export default defineNuxtPlugin(({ $pinia }) => {
  return {
    provide: {
      pinia: $pinia || createPinia(),
    },
  }
})
