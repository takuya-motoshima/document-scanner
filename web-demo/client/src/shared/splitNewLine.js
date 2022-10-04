/**
 * Split a string with a new line.
 */
export default str => {
  if (str == null)
    return str;
  return str
    .replace(/^[\s　]*\r?\n/gm, '')// Remove blank lines.
    .replace(/\r?\n$/, '')// Removed trailing line breaks.
    .replace(/^[\s　]+|[\s　]+$/gm, '')// Trim the space in each row.
    .split(/\r?\n/);
}