module.exports = {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        aurora: {
          navy: "#081120",
          ink: "#0b1324",
          ciano: "#22d3ee",
          violet: "#8b5cf6",
          lilac: "#c084fc",
          slate: "#94a3b8",
        },
      },
      boxShadow: {
        glass: "0 24px 80px rgba(8, 17, 32, 0.35)",
      },
      backgroundImage: {
        "aurora-grid":
          "radial-gradient(circle at top left, rgba(34, 211, 238, 0.10), transparent 28%), radial-gradient(circle at top right, rgba(139, 92, 246, 0.12), transparent 22%), radial-gradient(circle at bottom, rgba(192, 132, 252, 0.10), transparent 26%)",
      },
    },
  },
  plugins: [],
};
