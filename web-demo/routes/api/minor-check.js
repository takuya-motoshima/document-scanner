const router = require('express').Router();
const {PythonShell} = require('python-shell')
const {File, Media} = require('nodejs-shared');
const path = require('path');

router.post('/', async (req, res, next) => {
  try {
    imgPath = File.getTmpPath(Media.statDataUrl(req.body.image).type);
    Media.writeDataUrlToFile(imgPath, req.body.image);
    let matches = await new Promise((rslv, rej) => {
      PythonShell.run('scan_cli.py', {
        pythonPath: '/usr/local/bin/python3.9',
        scriptPath: path.resolve(global.APP_DIR, '../src'),
        args: ['-i', imgPath, '-t', req.body.type, '-f', 'age'],
        mode: 'text'
      }, (err, res) => {
        if (err)
          return void rej(err);
        rslv(res.join(''));
      });
    });
    matches = JSON.parse(matches || '{}');
    res.json(matches);
  } catch (err) {
    next(err);
  }
});
module.exports = router;