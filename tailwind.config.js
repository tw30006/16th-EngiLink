/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./templates/*.html",
    "./**/*.html",
    "./**/*.js"
  ],
  theme: {
    extend: {
      scrollMargin: {
        '16': '4rem',
      },
    },
  },
  plugins: [],
}

