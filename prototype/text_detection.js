const fs = require('fs');
const dotenv = require('dotenv');
const vision = require('@google-cloud/vision');

function loadEnv() {
  const envPath = `${__dirname}/../.env`;
  if (!fs.existsSync(envPath))
    throw new Error(`${envPath} not found`);
  return dotenv.parse(fs.readFileSync(envPath, 'utf8'));
}

function instantiateImageAnnotatorClient() {
  const env = loadEnv();
  if (!('GOOGLE_APPLICATION_CREDENTIALS' in env))
    throw new Error('GOOGLE_APPLICATION_CREDENTIALS not found in ".env"')
  const credentials = JSON.parse(env.GOOGLE_APPLICATION_CREDENTIALS);
  return new vision.ImageAnnotatorClient({credentials});
}

const client = instantiateImageAnnotatorClient();
// const imgPath = `${__dirname}/../img/blank.png`;
const imgPath = `${__dirname}/../img/driverslicense.png`;

client.documentTextDetection(imgPath).then(res => {
  if (!res[0].fullTextAnnotation)
    return void console.log('No text was found in the image');
  console.log(res[0].fullTextAnnotation.text.replace(/\n/g, ''));
  // page = res[0].fullTextAnnotation.pages[0];
  // let i = 0;
  // for (let block of page.blocks)
  //   for (let paragraph of block.paragraphs)
  //     for (let word of paragraph.words)
  //       for (let symbol of word.symbols)
  //         console.log(`${i++}: ${symbol.text}`)
});
