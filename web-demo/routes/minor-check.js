const router = require('express').Router();

router.get('/', (req, res) => {
  res.render('minor-check');
});
module.exports = router;