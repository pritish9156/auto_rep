const express = require('express');
const { exec } = require('child_process');

const app = express();
const port = 3000; // Specify the port number you want to use

app.get('/launch-tkinter', (req, res) => {
  exec('python auto_rep.py', (error) => {
    if (error) {
      console.error(`Error launching Tkinter: ${error.message}`);
      res.status(500).send('Error launching Tkinter');
      return;
    }
    
    console.log('Tkinter launched successfully');
    res.send('Tkinter launched successfully');
  });
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
  console.log(`http://localhost:3000/launch-tkinter`);

});
