export default {
  content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: "#0057ff",
        brand:  '#0057FF',
        accent: '#FF9900',
        stroke: '#D9E2F3',
        surface:'#EAF1FF',
      },
      borderRadius: {
        xl:  '24px',
        lg:  '12px',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
    }
  }
}
