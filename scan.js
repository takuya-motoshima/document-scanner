const {PythonShell} = require('python-shell');
const {program} = require('commander');
const utils = require('./utils');
const fs = require('fs');

// Parse arguments.
program
  .description('Scan document from image')
  .requiredOption('-i, --input <string>', 'Image path or Data URL', utils.validateImg)
  .option('-o, --output <string>', 'Output image path of the found document')
  .option('-r, --aspect <string>', 'Resize the scanned document to the specified aspect ratio. Typing as a width:height ratio (like 4:5 or 1.618:1).', utils.validateAspectRatio)
  .parse();
const opts = program.opts();

// Generate command arguments.
const args = ['-i', opts.input, '-p'];
if (opts.output)
  args.push('-o', opts.output);
if (opts.aspectRatio)
  args.push('-r', opts.aspectRatio);

// Scan document.
PythonShell.run('scan.py', {args}, (err, res) => {
  // Exception occurred in python.
  if (err)
    return void console.error(err.message);

  // If no document is found.
  if (!res)
    return void console.warn('Document not found in image');

  // Document data URL scanned from image.
  const dataURL = res[0];

  // Write document image to file.
  const b64 = dataURL.replace(/^data:image\/[A-Za-z]+;base64,/, '');
  console.log(`b64=${b64.slice(0, 100)}`);
  fs.writeFileSync('output/result.png', b64);

  // test
  {
    const tmp = fs.readFileSync('output/result2.png', {encoding: 'base64'});
    console.log(`tmp=${tmp.slice(0, 100)}`);
  }
});