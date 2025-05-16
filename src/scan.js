/*
read file
split on space
run regex through detector
save file and vuln regex to a new file
manually check that file for redos
*/

const fs = require('node:fs');
const path = require('node:path');
const { skip } = require('node:test');
const safeRegex = require('safe-regex');

const filePath = path.join(__dirname, '..', 'regex_results.txt');

fs.readFile(filePath, 'utf8', (err, data) => {
  if (err) {
	console.error('Error reading file:', err);
	return;
  }

  // Split into lines and extract regex-looking patterns
  const regexPattern = /(?<=\s|^|['"`])(\/(?!\/)(?:\\\/|[^\n\/])+\/[gimsuy]*)/g;

  const lines = data.split('\n');
  const regexSet = new Set();

  for (const line of lines) {
	const found = line.match(regexPattern);
	if (found) {
	  for (const regex of found) {
		regexSet.add(regex.trim());
	  }
	}
  }

  const uniqueRegexes = [...regexSet];
  const unsafeRegexes = [];

  for (const literal of uniqueRegexes) {
	try {
	  // Strip the leading and trailing `/`, extract flags
	  const lastSlash = literal.lastIndexOf('/');
	  const pattern = literal.slice(1, lastSlash);
	  const flags = literal.slice(lastSlash + 1);

	  if (!safeRegex(pattern)) {
		unsafeRegexes.push(literal);
	  }
	} catch{
		skip();
	}
  }
  fs.writeFileSync(path.join(__dirname, '..', 'unsafe_regexes.txt'), unsafeRegexes.join('\n'), 'utf8');
});