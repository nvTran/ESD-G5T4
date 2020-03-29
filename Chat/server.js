// const http = require('http') 
// var app = express()
// var server = require('http').createServer(app)
// var io = require('socket.io').listen(server)
// users = [];
// connections = [];

const io = require('socket.io')(3000)

// server.listen(process.env.PORT || 3000)

// app.get('/', function(req, res) {
//     res.sendFile(__dirname + '/index.html')
// });

// const fs = require('fs')
// const port = 5500

// const server = http.createServer(function(req, res) {
//     res.writeHead(200, {'content-Type':'text/html'})
//     fs.readFile('index.html', function(error, data) {
//         if (error) {
//             res.writeHead(404)
//             res.write('Error: File not found')
//         }
//         else {
//             res.write(data)
//         }
//         res.end() 

//     })
// })

// server.listen(port, function(error) {
//     if (error) {
//         console.log('Something is wrong', error)
//     }
//     else {
//         console.log('Server is listening on port ' + port)
//     }
// })

const users = {}

io.on('connection', socket => {
    // socket.emit('chat-message', 'Welcome')
    socket.on('new-user', name => {
        users[socket.id] = name
        socket.broadcast.emit('user-connected', name)
    })
    socket.on('send-chat-message', message => {
        socket.broadcast.emit('chat-message', { message: message, name: users[socket.id] })
    })
    socket.on('disconnect', () => {
        socket.broadcast.emit('user-disconnected', users[socket.id])
        delete users[socket.id]
    })
})