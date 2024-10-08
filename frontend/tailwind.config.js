/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["./public/index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
    theme: {
        extend: {},
    },
    plugins: [require("daisyui")],
    daisyui: {
        themes: ["lemonade", "forest"], //Only light and dark theme
        darkTheme: "forest",
        base: true,
        styled: true,
        prefix: "",
        logs: true,
        themeRoot: ":root",
    }
};
