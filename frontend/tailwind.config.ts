import type { Config } from "tailwindcss";

export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        brand: {
          green: "#4CAF50",
          teal: "#03DAC6",
          blue: "#03A9F4",
        },
      },
    },
  },
  plugins: [],
} satisfies Config;
