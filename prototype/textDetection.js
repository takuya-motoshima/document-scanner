const dotenv = require('dotenv');
const fs = require('fs');
const vision = require('@google-cloud/vision');
const moment = require('moment');

// Load .env.
const envPath = '../.env';
if (!fs.existsSync(envPath))
  throw new Error(`${envPath} not found`);
const config = dotenv.parse(fs.readFileSync(envPath, 'utf8'));

// Find google cloud credentials from ".env".
if (!('GOOGLE_APPLICATION_CREDENTIALS' in config))
  throw new Error('GOOGLE_APPLICATION_CREDENTIALS not found in ".env"')
const creds = JSON.parse(config.GOOGLE_APPLICATION_CREDENTIALS);

// Instantiates a client.
const client = new vision.ImageAnnotatorClient({credentials: creds});

(async () => {
  const imgPath = '../img/license_only_name_and_birthday.png';

  // Find text in images.
  let [res] = await client.documentTextDetection(imgPath);
  const doc = res.fullTextAnnotation;
  console.log(`doc.text=${doc.text.replace(/\n/g, '')}`);

  // Print the found characters one by one.
  page = doc.pages[0];
  for (let [i, block] of Object.entries(page.blocks))
    for (let [j, par] of Object.entries(block.paragraphs))
      for (let [k, word] of Object.entries(par.words))
        for (let [l, sym] of Object.entries(word.symbols))
          console.log(`block[${i}].paragraphs[${j}].word[${k}].symbol[${l}].text=${sym.text}`)
})();