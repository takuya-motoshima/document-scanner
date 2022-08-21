const router = require('express').Router();
const {PythonShell} = require('python-shell')
const {File, Media} = require('nodejs-shared');
const path = require('path');

router.post('/', async (req, res, next) => {
  try {
    // Invoke address normalization.
    let normalizedAddress = await new Promise((rslv, rej) => {
      PythonShell.run('address_normalization_cli.py', {
        pythonPath: '/usr/local/bin/python3.9',
        scriptPath: path.resolve(global.APP_DIR, '../src'),
        args: ['-i', req.body.address],
        mode: 'text'
      }, (err, res) => {
        if (err)
          return void rej(err);
        // Each newline in the python print result is stored in an array element and returned.
        rslv(res.join(''));
      });
    });

    // OCR results from json to object.
    normalizedAddress = JSON.parse(normalizedAddress || '{}');
    // console.log('normalizedAddress=', normalizedAddress);
    res.json(normalizedAddress);
  } catch (err) {
    next(err);
  }
});
module.exports = router;