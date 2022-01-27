const {PythonShell} = require('python-shell');
const {program} = require('commander');
const utils = require('./utils');

// Define arguments.
program
  .description('Scan document from image')
  .requiredOption('-i, --image <string>', 'Image path or Data URL', utils.validateImg)
  .option('-r, --aspect-ratio <string>', 'The scanned document will be resized to the specified aspect ratio, The format is W:H', utils.validateAspectRatio)
  .parse();

// Get an argument.
const opts = program.opts();
console.log('opts=', opts);

// // Run Python's Document Scan Module.
// PythonShell.run('scan.py', {args: [opts.image]}, (err, res) => {
//   if (err)
//     return void console.error(err.message);
//   console.log(res);
// });