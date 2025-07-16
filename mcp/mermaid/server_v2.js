import express from 'express';
import { writeFileSync, unlinkSync } from 'fs';
import { execSync } from 'child_process';
import { randomUUID } from 'crypto';

const app = express();
app.use(express.text({ type: '*/*', limit: '100kb' }));

app.post('/validate', (req, res) => {
  const text = req.body || '';
//   const fileName = `/tmp/${randomUUID()}.md`;
  const inputFileName = `/tmp/input.md`;
  const outputFileName = `/tmp/output.svg`;
  writeFileSync(inputFileName, text);

  let out = '', err = '';
  try {
    out = execSync(`mmdc -i ${inputFileName} -o ${outputFileName}`, {
      stdio: ['ignore','pipe','pipe']
    }).toString();

  } catch (e) {
    // if mmdc outright fails (e.g. not installed)
    err = e.stderr?.toString() || e.message;
  } finally {
    unlinkSync(inputFileName);
    // unlinkSync(outputFileName);
  }

  const combined = (out + err).toLowerCase();
  if (combined.includes('syntax error') || combined.includes('parse error')) {
    // extract the first offending line if you like
    const line = (out+err).split(/\r?\n/).find(l =>
      /syntax error|parse error/i.test(l)
    ) || 'Syntax error';
    return { valid: false, error: line.trim() };
  }
  return { valid: true };
  

//   try {
//     writeFileSync(inputFileName, text);
//     // Try rendering with mmdc to check validity
//     // execSync(`mmdc -i ${inputFileName} -o ${outputFileName} --failOnError`, { stdio: 'pipe' });
//     res.json({ valid: true });
//   } catch (err) {
//     const msg = err.stderr?.toString() || err.stdout?.toString() || err.message;
//     res.json({ valid: false, error: msg || 'Invalid diagram' });
//   } finally {
//     // Clean up output file if it exists
//     try {
//       unlinkSync(outputFileName);
//       unlinkSync(inputFileName);
//     } catch (e) {
//       // Ignore if file doesn't exist
//     }
//   }
});

app.get('/health', (_, res) => res.send('OK'));

app.listen(8000, () => console.log('Mermaid MCP Validator running on port 8000'));
