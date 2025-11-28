/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'alfa-red': '#EF3124',      // Основной красный
        'alfa-dark': '#0B1F35',     // Темный текст
        'alfa-gray': '#F3F4F5',     // Фон
      },
      fontFamily: {
        sans: ['Roboto', 'Inter', 'sans-serif'],
      }
    },
  },
  plugins: [],
}