const {PythonShell} = require('python-shell');
const {program, InvalidArgumentError} = require('commander');
const fs = require('fs');

// Parse arguments.
program
  .description('Scan the text of a document')
  .requiredOption('-i, --input <string>', 'Image path or Data URL', value => {
    const matches = value.match(/^\s*data:(?:(\w+\/[\w\d\-+.]+)(?:;[\w-]+=[\w\d-]+)?)?(?:;base64)?,([\w\d!$&\',()*+;=\-._~:@\/?%\s]*)\s*$/);
    if (matches) {
      const mime = matches[1];
      if (mime !== 'image/png' && mime !== 'image/jpeg')
        throw new InvalidArgumentError('Only jpeg or png can be used for the input DataURL');
    } else if (!fs.existsSync(value) || !fs.lstatSync(value).isFile())
      throw new InvalidArgumentError('File not found');
    return value;
  })
  .requiredOption('-t, --type <string>', 'OCR document type. \'driverslicense\' or \'mynumber\' can be used', value => {
    if (!['driverslicense', 'mynumber'].includes(value))
      throw new InvalidArgumentError('The type can be "driverslicense" or "mynumber"');
    return value;
  })
  .option('-d, --debug', 'Display debug image on display', false)
  // .option('-o, --output <string>', 'Output image path of the found document')
  // .option('-r, --aspect <string>', 'Resize the scanned document to the specified aspect ratio. Typing as a width:height ratio (like 4:5 or 1.618:1).', value => {
  //   const matches = value.match(/^((?!0\d)\d*(?:\.\d+)?):((?!0\d)\d*(?:\.\d+)?)$/);
  //   if (!matches)
  //     throw new InvalidArgumentError('The aspect ratio can be in the format "width:height"');
  //   const [_, wdRatio, htRatio] = matches;
  //   if (parseFloat(wdRatio) === 0 || parseFloat(htRatio) === 0)
  //     throw new InvalidArgumentError('Zero is not allowed for the aspect ratio width and height');
  //   return value;
  // })
  .parse();
const options = program.opts();

// Generate command arguments.
const args = ['-i', options.input,  '-t', options.type];

// Set optional parameters.
// if (options.output)
//   args.push('-o', options.output);
// if (options.aspect)
//   args.push('-r', options.aspect);
if (options.debug)
  args.push('-d');

// Invoke scan.
const scriptPath = __dirname;
let matches = await new Promise((rslv, rej) => {
  PythonShell.run('scan_cli.py', {
    // pythonPath: '/usr/local/bin/python3.9',
    scriptPath,
    args: ['-i', imgPath, '-t', 'driverslicense'],
    mode: 'text'
  }, (err, res) => {
    rslv(!err ? res : {});
  });
});
console.log(matches);