const io = require('socket.io')(3000)

io.on('connection', socket => {
    // socket.emit('chat-message', 'Welcome')
    socket.on('new-user', name => {
        users[socket.id] = name
        socket.broadcast.emit('user-connected', name)
    })
    socket.on('send-chat-message', message => {
        socket.broadcast.emit('chat-message', { message: message, name: users[socket.id] })
    })
    
})