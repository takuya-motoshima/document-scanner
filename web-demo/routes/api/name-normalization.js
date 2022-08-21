const router = require('express').Router();
const {PythonShell} = require('python-shell')
const {File, Media} = require('nodejs-shared');
const path = require('path');

router.post('/', async (req, res, next) => {
  try {
    // Invoke name normalization.
    let divideName = await new Promise((rslv, rej) => {
      PythonShell.run('name_normalization_cli.py', {
        pythonPath: '/usr/local/bin/python3.9',
        scriptPath: path.resolve(global.APP_DIR, '../src'),
        args: ['-i', req.body.name],
        mode: 'text'
      }, (err, res) => {
        if (err)
          return void rej(err);
        // Each newline in the python print result is stored in an array element and returned.
        rslv(res.join(''));
      });
    });

    // OCR results from json to object.
    divideName = JSON.parse(divideName || '{}');
    // console.log('divideName=', divideName);
    res.json(divideName);
  } catch (err) {
    next(err);
  }
});
module.exports = router;