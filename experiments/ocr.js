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
if (!('GOOGLE_CREDS' in config))
  throw new Error('GOOGLE_CREDS not found in ".env"')
const creds = JSON.parse(config.GOOGLE_CREDS);

// Instantiates a client.
const client = new vision.ImageAnnotatorClient({credentials: creds});

(async () => {
  const imgPath = '../img/license_only_name_and_birthday.png';

  // Find text in images.
  let [res] = await client.documentTextDetection(imgPath);
  const doc = res.fullTextAnnotation;
  console.log(`doc.text=${doc.text.replace(/\n/g, '')}`);
  const jsonPath = `output/${moment().format('YYYYMMDDHHmmss')}.json`;
  fs.writeFileSync(jsonPath, JSON.stringify(res, null, 2));
  console.log(`Write ${jsonPath}`);

  // Print the found characters one by one.
  page = doc.pages[0];
  for (let [i, block] of Object.entries(page.blocks))
    for (let [j, par] of Object.entries(block.paragraphs))
      for (let [k, word] of Object.entries(par.words))
        for (let [l, symbol] of Object.entries(word.symbols))
          // console.log(`symbol.text=${symbol.text}`);
          console.log(`block[${i}].paragraphs[${j}].word[${k}].symbol[${l}].text=${symbol.text}`)
})();