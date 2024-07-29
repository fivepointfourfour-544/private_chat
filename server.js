const WebSocket = require('ws');
const server = new WebSocket.Server({ port: 8080 });

const rooms = {};

server.on('connection', (ws, req) => {
    const key = req.url.slice(1); // Extract the key from the URL

    if (!rooms[key]) {
        rooms[key] = [];
    }

    if (rooms[key].length >= 2) {
        ws.close();
        return;
    }

    rooms[key].push(ws);

    ws.on('message', message => {
        rooms[key].forEach(client => {
            if (client !== ws && client.readyState === WebSocket.OPEN) {
                client.send(message);
            }
        });
    });

    ws.on('close', () => {
        rooms[key] = rooms[key].filter(client => client !== ws);
        if (rooms[key].length === 0) {
            delete rooms[key];
        }
    });
});
