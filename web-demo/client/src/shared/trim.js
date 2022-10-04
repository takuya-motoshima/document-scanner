/**
 * Trim string.
 */
export default str => {
  if (str == null)
    return str;
  return str
    .toString()
    .replace(/\r?\n/g, '')
    .replace(/^[\s　]+|[\s　]+$/g, '');
}