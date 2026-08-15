const fs = require('fs');
const path = require('path');

const stylesPath = path.join(__dirname, 'styles.css');
const content = fs.readFileSync(stylesPath, 'utf8');

const lines = content.split('\n');
lines.forEach((line, idx) => {
  if (line.includes('main') || line.includes('max-w')) {
    console.log(`Line ${idx + 1}: ${line.trim()}`);
  }
});
