const fs = require('fs');
let html = fs.readFileSync('extracted_original.html', 'utf8');
html = html.replace(/```jsx/g, '');
html = html.replace(/```javascript/g, '');
html = html.replace(/```html/g, '');
html = html.replace(/```css/g, '');
html = html.replace(/```/g, '');
fs.writeFileSync('extracted_original.html', html, 'utf8');
console.log('Cleaned markdown');
