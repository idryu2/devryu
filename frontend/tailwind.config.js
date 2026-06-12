/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        critical: "#dc2626",
        warning: "#d97706",
        info: "#2563eb",
      },
    },
  },
  plugins: [],
};
