const express = require('express');
const bodyParser = require('body-parser');
const util = require('util');
const sleep = util.promisify(setTimeout);
const app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended:false}));
app.use(express.static('views'));
app.use(express.static('public'));
app.set('view engine', 'ejs');

const hostname = '10.255.188.104';
const port = 8080;

app.get('/', function (req, res) {
	res.render('index');
})

app.listen(8080, function() {
	console.log(`Server running at http://${hostname}:${port}/`);
})

app.get('/signIn', function (req, res) {
	res.render('login_page.ejs');
})

app.get('/reqStart', function (req, res) {
	const exec = require("child_process").exec;
	exec("cd views ; ./runGPS.sh", (err,stdout,stderr) => { });
	res.render('data_processing.ejs');
})

app.get('/reqStop', function (req, res) {
	const exec = require("child_process").exec;
	exec("sudo killall python3.7", (err,stdout,stderr) => { });
	res.render('data_processing.ejs');
})

app.post('/login', function (req, res) {
	if(req.body.username === "pi" && req.body.pwd === "raspberry2") {
		res.render('data_processing.ejs');
	} else {
		res.render('login_fail.ejs');
	}
})

app.get('/saveData', function (req, res) {
	const exec = require("child_process").exec;
	exec("cd views ; sudo ./save", (err,stdout,stderr) => { });
	res.render('data_processing.ejs');
})

app.get('/processing', function (req, res) {
	res.render('data_processing.ejs');
})

app.get('/securityCheck', function (req, res) {
	res.render('security_check.ejs');
})

app.get('/stats', async function (req, res) {
	const exec = require("child_process").exec;
	exec("cd views ; sudo python3.7 elevation.py ; sudo python3.7 euclid_dist.py", (err,stdout,stderr) => { });
	await sleep(1000);
	res.render('stats.ejs');
})
