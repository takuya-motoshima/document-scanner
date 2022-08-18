const router = require('express').Router();

router.get('/', (req, res) => {
  res.render('ocr');
});
module.exports = router;