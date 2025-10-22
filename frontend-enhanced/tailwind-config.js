// tailwind.config.js
// Tailwind CSS configuration with custom animations and theme colors

/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        // Light Mode Colors
        "primary-light": "#29FF2C", // rgb(41, 255, 44)
        "accent-light": "#10B981",
        "bg-light": "#FFFFFF",
        "text-light": "#1A1A1A",

        // Dark Mode Colors
        "primary-dark": "#2EB9FF", // rgb(46, 185, 255)
        "accent-dark": "#3B82F6",
        "bg-dark": "#0A0A0A",
        "text-dark": "#FFFFFF",
      },
      animation: {
        gradient: "gradient 8s linear infinite",
        float: "float 6s ease-in-out infinite",
        splash: "splash 0.6s ease-out",
        "star-border": "star-border 3s linear infinite",
        "pulse-slow": "pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite",
      },
      keyframes: {
        gradient: {
          "0%, 100%": { "background-position": "0% 50%" },
          "50%": { "background-position": "100% 50%" },
        },
        float: {
          "0%, 100%": { transform: "translateY(0px)" },
          "50%": { transform: "translateY(-20px)" },
        },
        splash: {
          "0%": { transform: "scale(0)", opacity: "1" },
          "100%": { transform: "scale(2)", opacity: "0" },
        },
        "star-border": {
          "0%": { transform: "rotate(0deg)" },
          "100%": { transform: "rotate(360deg)" },
        },
      },
      backgroundImage: {
        "gradient-light":
          "linear-gradient(90deg, #29FF2C 0%, #10B981 50%, #059669 100%)",
        "gradient-dark":
          "linear-gradient(90deg, #2EB9FF 0%, #3B82F6 50%, #6366F1 100%)",
      },
    },
  },
  plugins: [],
};
