const {PythonShell} = require('python-shell');

PythonShell.run('pythonShell.py', {
  // pythonPath: '/usr/bin/python3.8',
  args: ['jhon']
}, async (err, res) => {
  if (err)
    return void console.error(err.message);
  console.log(res);
});