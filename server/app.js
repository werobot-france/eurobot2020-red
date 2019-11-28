const express = require('express')
const app = express()
const server = require('http').Server(app)
const io = require('socket.io')(server)

server.listen(3002, () => {
    console.log('server listening')
})

app.use('/', express.static('../dash/build'))

app.get('/api', (req, res) => {
  res.json({success: true})
})

io.on('connection', (socket) => {
  socket.emit('news', { hello: 'world' })
  socket.on('my other event', (data) => {
    console.log(data);
  })
})