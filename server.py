from flask import Flask
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Store active rooms with their codes
rooms_with_codes = {}

@socketio.on('create_or_join')
def create_or_join(data):
    username = data['username']
    room = data['room']
    code = data.get('code')  # Get the room code
    is_new_room = data.get('is_new_room', False)

    if is_new_room:  # User wants to create a new room
        if room in rooms_with_codes:
            emit('room_error', {'message': 'Room already exists. Choose a different name.'})
        else:
            rooms_with_codes[room] = code  # Set the room code
            join_room(room)
            emit('room_created', {'message': f"Room '{room}' created successfully!"})
    else:  # User wants to join an existing room
        if room not in rooms_with_codes:
            emit('room_error', {'message': 'Room does not exist.'})
        elif rooms_with_codes[room] != code:
            emit('room_error', {'message': 'Incorrect room code.'})
        else:
            join_room(room)
            emit('room_joined', {'message': f"{username} joined room: {room}"}, to=room)

@socketio.on('send_message')
def handle_message(data):
    username = data['username']
    message = data['message']
    room = data['room']
    emit('receive_message', {'username': username, 'message': message}, to=room)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
