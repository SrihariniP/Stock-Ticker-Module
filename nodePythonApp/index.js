const express = require('express')
const {spawn} = require('child_process');
const bodyParser = require('body-parser')
const http = require('http');
const cors = require('cors');


const app = express()
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(express.static("my-cart1"));
app.use(cors({origin: '*'}));

const port = 3000

app.get('/', (req, res) => {
    var cmp = (req.body).companyName;
    console.log(cmp);
 /*var dataToSend;
 // spawn new child process to call the python script
 const python = spawn('python', ['script1.py','INFY']);
 // collect data from script
 python.stdout.on('data', function (data) {
  console.log('Pipe data from python script ...');
  dataToSend = data.toString();
 });
 // in close event we are sure that stream from child process is closed
 python.on('close', (code) => {
 console.log(`child process close all stdio with code ${code}`);
 // send data to browser
 res.send(dataToSend)
 });
 */

 res.send("This is the Home Page");

 console.log("I'm here");
})

app.post("/market", async function(req, res, next){
    var cmp = (req.body).companyName;
    console.log(cmp);
    //res.send("Hello World");
    //const rand = await python("./random_choices.py");
    //console.log(await rand.get_random_word());
    //python.exit();
    
    var dataToSend;
    const python = spawn('python', ['app.py',cmp]);
    python.stdout.on('data', function (data) {
        console.log('Pipe data from python script ...');
        console.log(data);
        dataToSend = data.toString();
    });

    python.on('close', (code) => {
        console.log(`child process close all stdio with code ${code}`);
        // send data to browser
        res.send(dataToSend)
        //res.send(dataToSend)
    });
    

    /*
    res.send({
        apple:2,
        orange: 10,
        graphData: dataToSend
    })
    */
})


app.listen(port, () => console.log(`Example app listening on port 
${port}!`))