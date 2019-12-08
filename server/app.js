const express = require('express')
const app = express()
const server = require('http').Server(app)
const io = require('socket.io')(server)
const gritty = require('gritty')
const expressHttpProxy = require('express-http-proxy')

server.listen(3002, () => {
    console.log('server listening')
})

//app.use('/', express.static('../dash/build'))

//app.use(gritty())

const PythonManager = require('./src/PythonManager')

const manager = new PythonManager()

manager.startProcess()

//{"cmd":"goto", "args": {"x": 1500, "y": 742}}

app.use('/', expressHttpProxy('http://localhost:3000'))

app.get('/api', (req, res) => {
  res.json({success: true})
})

io.on('connection', (socket) => {
  socket.emit('news', { hello: 'world' })
  socket.on('goto', (data) => {
    console.log('Goto:', data);
    manager.write('goto', data)
  })
  socket.on('motors', (data) => {
    console.log('motors');
    manager.write('motors', data)
  })
  socket.on('stop', (data) => {
    console.log('Stop');
    manager.write('stop')
  })
})
// gritty.listen(io, {
//     command: 'ci',
//     autoRestart: true
// });
