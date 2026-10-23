// Vercel 빌드 시 환경변수 API_BASE_URL → config.js 생성
const fs = require("fs");
const url = (process.env.API_BASE_URL || "http://localhost:8000").replace(/\/$/, "");
fs.writeFileSync("config.js", `window.APP_CONFIG = { API_BASE_URL: ${JSON.stringify(url)} };\n`);
console.log("config.js generated:", url);
