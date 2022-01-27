const commander = require('commander');
const fs = require('fs');

// Image option validation.
exports.validateImg = (val) => {
  const found = val.match(/^\s*data:(?:(\w+\/[\w\d\-+.]+)(?:;[\w-]+=[\w\d-]+)?)?(?:;base64)?,([\w\d!$&\',()*+;=\-._~:@\/?%\s]*)\s*$/);
  if (found) {
    const mediaType = found[1];
    if (mediaType !== 'image/png' && mediaType !== 'image/jpeg')
      throw new commander.InvalidArgumentError('Unsupported media type, Images can process PNG or JPG.');
  } else {
    if (!fs.existsSync(val))
      throw new commander.InvalidArgumentError('File path not found.');
    else if (!fs.lstatSync(val).isFile())
      throw new commander.InvalidArgumentError('It\'s not a file path.');
  }
  return val;
}

// Aspect ratio option validation
exports.validateAspectRatio = (val) => {
  const found = val.match(/^((?!0\d)\d*(?:\.\d+)?):((?!0\d)\d*(?:\.\d+)?)$/);
  if (!found)
    throw new commander.InvalidArgumentError('Invalid format, typing as a width:height ratio (like 4:5 or 1.618:1).');
  const [_, w, h] = found;
  if (parseFloat(w) === 0 || parseFloat(h) === 0)
    throw new commander.InvalidArgumentError('Zero cannot be used for height or width ratio.');
  return val;
}