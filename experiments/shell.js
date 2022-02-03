const {PythonShell} = require('python-shell');

PythonShell.run('shell.py', {args: ['jhon']}, async (err, res) => {
  if (err)
    return void console.error(err.message);
  console.log(res);
});