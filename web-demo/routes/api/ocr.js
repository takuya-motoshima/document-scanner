const router = require('express').Router();
const {PythonShell} = require('python-shell')
const {File, Media} = require('nodejs-shared');
const path = require('path');

router.post('/', async (req, res, next) => {
  try {
    // Write DataURL as an image file.
    imgPath = File.getTmpPath(Media.statDataUrl(req.body.image).type);
    Media.writeDataUrlToFile(imgPath, req.body.image);

    // Invoke scan.
    const scriptPath = path.resolve(global.APP_DIR, '../src');
    let matches = await new Promise((rslv, rej) => {
      PythonShell.run('scan_cli.py', {
        pythonPath: '/usr/local/bin/python3.9',
        scriptPath,
        args: ['-i', imgPath, '-t', req.body.type],
        mode: 'text'
      }, (err, res) => {
        if (err)
          return void rej(err);
        // Each newline in the python print result is stored in an array element and returned.
        rslv(res.join(''));
      });
    });

    // OCR results from json to object.
    matches = JSON.parse(matches || '{}');
    console.log('matches=', matches);
    res.json(matches);
  } catch (err) {
    console.error(err);
    next(err);
  }
});
module.exports = router;