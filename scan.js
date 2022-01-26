const {PythonShell} = require('python-shell');
const {program} = require('commander');

// Define arguments.
program
  .description('Scan document from image')
  .requiredOption('-i, --image <image>', 'Image path or Data URL')
  .parse();

// Get an argument.
const opts = program.opts();
// console.log('opts=', opts);

// Run Python's Document Scan Module.
PythonShell.run('scan.py', {args: [opts.image]}, (err, res) => {
  if (err)
    return void console.error(err.message);
  console.log(res);
});