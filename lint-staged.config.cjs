"use strict";

const actions = [
  "prettier --write", 
  // "eslint --cache --ext .js,.jsx,.ts,.tsx"
];

module.exports = {
  // "*.json": ["npm run _pretty:json:write --"],
  "*.{js,ts,tsx,!*.config.сjs}": actions
};
