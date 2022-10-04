const {PythonShell} = require('python-shell');
const {program, InvalidArgumentError} = require('commander');
const fs = require('fs');

function getArgs() {
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
    .parse();
  return program.opts();
}
const args = getArgs();
const pythonArgs = ['-i', args.img, '-t', args.type];
if (args.debug)
  pythonArgs.push('-d');
let matches = await new Promise((rslv, rej) => {
  PythonShell.run('scan_cli.py', {
    // pythonPath: '/usr/local/bin/python3.9',
    scriptPath: __dirname,
    args: pythonArgs,
    mode: 'text'
  }, (err, res) => {
    if (err)
      return void rej(err);
    rslv(res);
  });
});
console.log(matches);