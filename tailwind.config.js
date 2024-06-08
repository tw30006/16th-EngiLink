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
      colors: {
        'user-blue': '#0D4295',
        'company-green': '#008F77',
      },
    },
  },
  plugins: [],
}

