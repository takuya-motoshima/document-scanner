const {PythonShell} = require('python-shell');
const {program} = require('commander');
const utils = require('./utils');

// Parse arguments.
program
  .description('Scan document from image')
  .requiredOption('-i, --image <string>', 'Image path or Data URL', utils.validateImg)
  .option('-r, --aspect-ratio <string>', 'Resize the scanned document to the specified aspect ratio. Typing as a width:height ratio (like 4:5 or 1.618:1).', utils.validateAspectRatio)
  .parse();
const opts = program.opts();
console.log('opts=', opts);

// // Run Python's Document Scan Module.
// PythonShell.run('scan.py', {args: [opts.image]}, (err, res) => {
//   if (err)
//     return void console.error(err.message);
//   console.log(res);
// });