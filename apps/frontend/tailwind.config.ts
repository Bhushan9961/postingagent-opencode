import type { Config } from "tailwindcss"

export default {
  darkMode: "class",
  content: [
    "./components/**/*.{vue,ts}",
    "./layouts/**/*.{vue,ts}",
    "./pages/**/*.{vue,ts}",
    "./app.vue",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: "#eff6ff",
          100: "#dbeafe",
          500: "#3b82f6",
          600: "#2563eb",
          700: "#1d4ed8",
        },
      },
    },
  },
  plugins: [],
} satisfies Config
