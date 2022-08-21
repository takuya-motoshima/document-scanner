const router = require('express').Router();

router.get('/', (req, res) => {
  res.render('name-normalization');
});
module.exports = router;