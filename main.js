const {PythonShell} = require('python-shell');

PythonShell.run('test.py', {args: ['Robin']}, (err, results) => {
  if (err)
    return void console.error(err.message);
  console.log(results);
});