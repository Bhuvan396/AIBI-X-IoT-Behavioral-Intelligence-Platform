/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        cyber: {
          dark: '#0a0b10',
          panel: '#151722',
          blue: '#3b82f6',
          cyan: '#06b6d4',
          accent: '#8b5cf6',
          danger: '#ef4444'
        }
      }
    },
  },
  plugins: [],
}
