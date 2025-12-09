/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    colors: {
      white: "#ffffff",
      black: "#000000",

      agriBg: "#f6fff0",
      agriGreen: "#2e7d32",
      agriSoil: "#8d6e63",
      agriWater: "#4fc3f7",
      agriSky: "#90caf9",
    },
    extend: {
      boxShadow: {
        agri: "0 0 3px rgba(0,0,0,0.15)",
      },
    },
  },
  plugins: [],
};
