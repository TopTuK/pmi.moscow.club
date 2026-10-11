module.exports = {
    testEnvironment: "jsdom",
    testEnvironmentOptions: {
        url: "https://pmi.moscow",
    },
    roots: ["<rootDir>/static/js"],
    testMatch: ["**/__tests__/**/*.test.js"],
    transform: {
        "^.+\\.js$": "babel-jest",
        "^.+\\.vue$": "@vue/vue2-jest",
    },
    moduleFileExtensions: ["js", "json", "vue"],
    collectCoverageFrom: [
        "static/js/**/*.js",
        "static/js/components/**/*.vue",
        "!static/js/__tests__/**",
        "!static/js/vendor/**",
        "!static/js/main.js",
    ],
    coverageDirectory: "<rootDir>/coverage",
};
