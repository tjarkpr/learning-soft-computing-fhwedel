var express = require('express');
var router = express.Router();
const { resolve } = require('path');
const { exec } = require('child_process');
const pathToChildProcess = resolve() + '/child_process/evaluate.sh';

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', {
    evaluationURL: req.baseUrl + '/evaluate',
  });
});

/* POST home page. */
router.post('/evaluate', function(req, res, next) {
  exec('"' + pathToChildProcess + '" "' + req.body.text + '"', (error, stdout, stderr) => {
    if (error || stderr) {
      res.json({status: 'error'});
      return;
    }
    let response = JSON.parse(stdout);
    res.json({status: 'ok', input: response.input, result: response.result, probability: response.probability});
  });
});

module.exports = router;
