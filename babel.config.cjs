module.exports = {
  presets: [
    // Enable parsing TypeScript syntax in tests (babel-jest)
    ["@babel/preset-typescript"],
    ["@babel/preset-env", { targets: { node: "current" } }],
    ["@babel/preset-react", { runtime: "automatic" }],
  ],
};
