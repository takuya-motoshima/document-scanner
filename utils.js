const commander = require('commander');
const fs = require('fs');

/**
 * Image option validation.
 *
 * @param   {string} Argument value.
 * @returns Returns the original value if there are no errors.
 * @throws  {commander.InvalidArgumentError} Invalid value.
 */
exports.validateImg = (val) => {
  const found = val.match(/^\s*data:(?:(\w+\/[\w\d\-+.]+)(?:;[\w-]+=[\w\d-]+)?)?(?:;base64)?,([\w\d!$&\',()*+;=\-._~:@\/?%\s]*)\s*$/);
  if (found) {
    const mime = found[1];
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

/**
 * Aspect ratio option validation.
 *
 * @param   {string} Argument value.
 * @returns Returns the original value if there are no errors.
 * @throws  {commander.InvalidArgumentError} Invalid value.
 */
exports.validateAspectRatio = (val) => {
  const found = val.match(/^((?!0\d)\d*(?:\.\d+)?):((?!0\d)\d*(?:\.\d+)?)$/);
  if (!found)
    throw new commander.InvalidArgumentError('Invalid format, typing as a width:height ratio (like 4:5 or 1.618:1)');
  const [_, wdRatio, htRatio] = found;
  if (parseFloat(wdRatio) === 0 || parseFloat(htRatio) === 0)
    throw new commander.InvalidArgumentError('Zero cannot be used for height or width ratio');
  return val;
}