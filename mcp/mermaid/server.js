import express from 'express';
import mermaid from 'mermaid';
import DOMPurify from "isomorphic-dompurify";

// Patch DOMPurify to avoid 'addHook is not a function' error
globalThis.DOMPurify = {
  addHook: () => {}
};

// Initialize mermaid
mermaid.initialize({
  startOnLoad: false,
  securityLevel: 'loose'  // needed for non-browser env
});

const app = express();
const PORT = process.env.PORT || 8000;

// Accept raw text bodies
app.use(express.text({ type: '*/*', limit: '10mb' }));

/**
 * POST /validate
 * Request body: raw Mermaid diagram text
 * Response: { valid: boolean, error?: string }
 */
app.post('/validate', async (req, res) => {
  const diagramText = req.body || '';
  // const clean = DOMPurify.sanitize(diagramText);
  // const clean = DOMPurify.sanitize(`<p>${diagramText}</p>`, { USE_PROFILES: { html: true } });
  console.log('Received diagram text:', diagramText);
  try {
    // parse throws on invalid syntax
    await mermaid.parse(diagramText);
    res.json({ valid: true});
  } catch (err) {
    // err.str contains detailed message in some versions, fallback to err.message
    const message = err.str || err.message || 'Unknown parse error';
    res.json({ valid: false, error: message });
  }
});

// Health check
app.get('/health', (req, res) => {
  res.send('OK');
});

app.listen(PORT, () => {
  console.log(`Mermaid Validator listening on port ${PORT}`);
});