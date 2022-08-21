const router = require('express').Router();

router.get('/', (req, res) => {
  res.render('address-normalization');
});
module.exports = router;