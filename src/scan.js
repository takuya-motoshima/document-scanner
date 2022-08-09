const {PythonShell} = require('python-shell');
const {program} = require('commander');
const commander = require('commander');
const fs = require('fs');
const moment = require('moment');

/**
 * Image option validation.
 *
 * @param   {string} Argument value.
 * @returns Return the original value if there are no errors.
 * @throws  {commander.InvalidArgumentError} Invalid value.
 */
function validateImg(val) {
  const matches = val.match(/^\s*data:(?:(\w+\/[\w\d\-+.]+)(?:;[\w-]+=[\w\d-]+)?)?(?:;base64)?,([\w\d!$&\',()*+;=\-._~:@\/?%\s]*)\s*$/);
  if (matches) {
    const mime = matches[1];
    if (mime !== 'image/png' && mime !== 'image/jpeg')
      throw new commander.InvalidArgumentError('Unsupported media type, Images can process PNG or JPG');
  } else {
    if (!fs.existsSync(val))
      throw new commander.InvalidArgumentError('File path not found');
    else if (!fs.lstatSync(val).isFile())
      throw new commander.InvalidArgumentError('It\'s not a file path');
  }
  return val;
}

// /**
//  * Aspect ratio option validation.
//  *
//  * @param   {string} Argument value.
//  * @returns Return the original value if there are no errors.
//  * @throws  {commander.InvalidArgumentError} Invalid value.
//  */
// function validateAspectRatio(val) {
//   const matches = val.match(/^((?!0\d)\d*(?:\.\d+)?):((?!0\d)\d*(?:\.\d+)?)$/);
//   if (!matches)
//     throw new commander.InvalidArgumentError('Invalid format, typing as a width:height ratio (like 4:5 or 1.618:1)');
//   const [_, wdRatio, htRatio] = matches;
//   if (parseFloat(wdRatio) === 0 || parseFloat(htRatio) === 0)
//     throw new commander.InvalidArgumentError('Zero cannot be used for height or width ratio');
//   return val;
// }

/**
 * Type option validation.
 *
 * @param   {string} Argument value.
 * @returns Return the original value if there are no errors.
 * @throws  {commander.InvalidArgumentError} Invalid value.
 */
function validateType(val) {
  if (!['driverslicense', 'mynumber'].includes(val))
    throw new commander.InvalidArgumentError('The type option can use \'driverslicense\' or \'mynumber\'');
  return val;
}

// Parse arguments.
program
  .description('Scan document from image')
  .requiredOption('-i, --input <string>', 'Image path or Data URL', validateImg)
  .option('-o, --output <string>', 'Output image path of the found document')
  // .option('-r, --aspect <string>', 'Resize the scanned document to the specified aspect ratio. Typing as a width:height ratio (like 4:5 or 1.618:1).', validateAspectRatio)
  .requiredOption('-t, --type <string>', 'OCR document type. \'driverslicense\' or \'mynumber\' can be used', validateType)
  .option('-d, --debug', 'Display debug image on display', false)
  .parse();
const options = program.opts();

// Generate command arguments.
const args = [
  '-i', options.input,
  '-p',
  '-t', options.type];
if (options.output)
  args.push('-o', options.output);
// if (options.aspect)
//   args.push('-r', options.aspect);
if (options.debug)
  args.push('-d');

// Scan document.
PythonShell.run(`${__dirname}/scan.py`, {args}, (err, res) => {
  // Exception occurred in python.
  if (err)
    return void console.error(err.message);

  // If no document is found.
  if (!res)
    return void console.warn('Document not found in image');

  // Base64 of scanned document image.
  const b64 = res.toString();
  console.log(`b64=${b64.slice(0, 100)}`);

  // Write document image to file.
  const outputFile = `logs/${moment().format('YYYYMMDDHHmmss')}.png`;
  fs.writeFileSync(outputFile, Buffer.from(b64, 'base64'));
  console.log(`Wtite ${outputFile}`);
});