const express = require('express')
const app = express()
const server = require('http').Server(app)
const io = require('socket.io')(server)
const gritty = require('gritty')

server.listen(3002, () => {
    console.log('server listening')
})

app.use('/', express.static('../dash/build'))

app.use(gritty())

app.get('/api', (req, res) => {
  res.json({success: true})
})

io.on('connection', (socket) => {
  socket.emit('news', { hello: 'world' })
  socket.on('my other event', (data) => {
    console.log(data);
  })
})

const PythonManager = require('./src/PythonManager')

const manager = new PythonManager()
 
gritty.listen(io, {
    command: 'ci',
    autoRestart: true
});
