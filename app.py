from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit
from pymongo import MongoClient
from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'SOME_SECRET_KEY'  # for session

# Initialize SocketIO
socketio = SocketIO(app)  # can pass cors_allowed_origins="*" for cross-domain

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client['hw2_db']
users_collection = db['users']


@app.route('/', methods=['GET', 'POST'])
def login():
    """
    Login route:
      - GET: shows the login form
      - POST: verifies username and password (hashed check), logs in on success
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Find the user by username only
        user = users_collection.find_one({'username': username})
        if user and check_password_hash(user['password'], password):
            # Correct password => store session info
            session['user_id'] = str(user['_id'])
            return redirect(url_for('profile'))
        else:
            return "Invalid credentials!", 401
    else:
        # GET => show login form
        return render_template('login.html')


@app.route('/profile')
def profile():
    """
    Profile route:
      - Accessible only if the user is logged in (checks session).
      - Displays the user's username (and possibly more info).
    """
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Retrieve user doc from DB
    user = users_collection.find_one({'_id': ObjectId(session['user_id'])})
    return render_template('profile.html', username=user['username'])


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Registration route:
      - GET: shows the registration form
      - POST: creates a new account with hashed password if username not taken
      - Broadcasts a 'new_user' SocketIO event to all connected clients
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = users_collection.find_one({'username': username})
        if existing_user:
            return "Username already taken!", 400

        # Hash the password before storing
        hashed_pw = generate_password_hash(password)

        new_user = {
            'username': username,
            'password': hashed_pw,
            'profile_pic': 'default_profile.png'
        }
        users_collection.insert_one(new_user)

        # Emit a SocketIO event to ALL connected clients (real-time notification)
        socketio.emit('new_user', {'username': username}, broadcast=True)

        return redirect(url_for('login'))
    else:
        # GET => render registration form
        return render_template('register.html')


@app.route('/logout')
def logout():
    """
    Logout route:
      - Pops 'user_id' from session and redirects to login
    """
    session.pop('user_id', None)
    return redirect(url_for('login'))


@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    """
    Password change route:
      - GET: shows form
      - POST: checks old password (hashed check) and updates to new hashed password
    """
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        old_pw = request.form['old_password']
        new_pw = request.form['new_password']

        user = users_collection.find_one({'_id': ObjectId(session['user_id'])})

        # Check old password with the hash stored in DB
        if user and check_password_hash(user['password'], old_pw):
            # Hash the new password
            hashed_new = generate_password_hash(new_pw)

            users_collection.update_one(
                {'_id': user['_id']},
                {'$set': {'password': hashed_new}}
            )
            return "Password updated successfully!"
        else:
            return "Incorrect old password!", 400
    else:
        # GET => render change_password form
        return render_template('change_password.html')


if __name__ == '__main__':
    # Run the Flask+SocketIO app
    socketio.run(app, debug=True)
