/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["./public/index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
    theme: {
        extend: {},
    },
    plugins: [require("daisyui")],
    daisyui: {
        themes: [
            {
                'my-light': {
                    'primary' : '#66cc8a',
                    'primary-focus' : '#41be6d',
                    'primary-content' : '#f9fafb',

                    'secondary' : '#006b60',
                    'secondary-focus' : '#014b44',
                    'secondary-content' : '#f9fafb',

                    'accent' : '#4b8078',
                    'accent-focus' : '#3a645d',
                    'accent-content' : '#f9fafb',

                    'neutral' : '#333c4d',
                    'neutral-focus' : '#1f242e',
                    'neutral-content' : '#f9fafb',

                    'base-100' : '#ffffff',
                    'base-200' : '#e3e6e8',
                    'base-300' : '#d4d4d4',
                    'base-content' : '#333c4d',

                    'info' : '#1c92f2',
                    'success' : '#009485',
                    'warning' : '#ff9900',
                    'error' : '#ff5724',

                    '--rounded-box': '1rem',          
                    '--rounded-btn': '.5rem',        
                    '--rounded-badge': '1.9rem',      

                    '--animation-btn': '0',       
                    '--animation-input': '0',       

                    '--btn-text-case': 'uppercase',   
                    '--navbar-padding': '.5rem',      
                    '--border-btn': '1px',       
                },
            }, {
                'my-dark': {
                    'primary' : '#55a548',
                    'primary-focus' : '#376a2f',
                    'primary-content' : '#ffffff',

                    'secondary' : '#1b716e',
                    'secondary-focus' : '#145250',
                    'secondary-content' : '#ffffff',

                    'accent' : '#bac03c',
                    'accent-focus' : '#8e932f',
                    'accent-content' : '#000000',

                    'neutral' : '#2a2a37',
                    'neutral-focus' : '#16181d',
                    'neutral-content' : '#ffffff',

                    'base-100' : '#282c34',
                    'base-200' : '#1f2228',
                    'base-300' : '#16181d',
                    'base-content' : '#ebecf0',

                    'info' : '#38b6ff',
                    'success' : '#7bc828',
                    'warning' : '#dbac48',
                    'error' : '#ff4d4d',

                    '--rounded-box': '1.5rem',
                    '--rounded-btn': '1.5rem',
                    '--rounded-badge': '1.5rem',

                    '--animation-btn': '.25s',
                    '--animation-input': '.2s',

                    '--btn-text-case': 'uppercase',
                    '--navbar-padding': '.5rem',
                    '--border-btn': '1.5px',
                },
            },
        ],
        darkTheme: 'my-dark',
        base: true,
        styled: true,
        prefix: "",
        logs: true,
        themeRoot: ":root",
    }
};
