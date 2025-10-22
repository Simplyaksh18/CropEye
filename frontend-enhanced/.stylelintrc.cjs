module.exports = {
  extends: ["stylelint-config-standard", "stylelint-config-tailwindcss"],
  // project specific overrides can go here
  rules: {
    "at-rule-no-unknown": [
      true,
      {
        ignoreAtRules: [
          "tailwind",
          "apply",
          "variants",
          "responsive",
          "screen",
        ],
      },
    ],
  },
};
