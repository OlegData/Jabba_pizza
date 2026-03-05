module.exports = {
  testEnvironment: "jsdom",
  transform: {
    "^.+\\.[jt]sx?$": "babel-jest",
    "^.+\\.mjs$": "babel-jest",
  },
  setupFiles: ["whatwg-fetch", "<rootDir>/jest.setup.cjs"],
  setupFilesAfterEnv: ["@testing-library/jest-dom"],
  transformIgnorePatterns: [
    "/node_modules/(?!(msw|@mswjs|until-async)/)",
  ],
};
