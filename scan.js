const {PythonShell} = require('python-shell');
const {program} = require('commander');
const utils = require('./utils');

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
  if (err)
    return void console.error(err.message);
  if (!res)
    return void console.warn('Document not found in image');
  const dataURL = res[0];
  console.log(`dataURL=${dataURL.slice(0, 100)}`);
});