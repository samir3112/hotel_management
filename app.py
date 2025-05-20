from flask import Flask, render_template, request, url_for, redirect, flash, session
from flask_mysqldb import MySQL
from datetime import datetime
import os

app = Flask(__name__)

# Secret key for session management
app.secret_key = os.urandom(24)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default_secret')

# Docker-based MySQL connection
app.config['MYSQL_HOST'] = 'db'  # Docker Compose service name
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'hotel_db'

mysql = MySQL(app)

# Helper function to get user_id from username
def get_user_id(username):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    return user[0] if user else None

# Home page showing rooms
@app.route('/')
def home():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM rooms")
    data = cursor.fetchall()
    rooms = []
    for row in data:
        rooms.append({
            'id': row[0],
            'name': row[1],
            'description': row[2],
            'price': row[3],
            'image': row[4]
        })
    return render_template('index.html', rooms=rooms)


# Room details page
@app.route('/room/<int:room_id>')
def room_detail(room_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM rooms WHERE id = %s", (room_id,))
    room = cursor.fetchone()
    cursor.close()
    if room:
        room_data = {
            'id': room[0],
            'name': room[1],
            'description': room[2],
            'price': room[3],
            'image': room[4],
            'facility': room[5]
        }
        return render_template('room_detail.html', room=room_data)
    else:
        flash('Room not found!', 'danger')
        return redirect(url_for('home'))

# Booking form for a specific room
@app.route('/book/<int:room_id>', methods=['GET', 'POST'])
def book_room(room_id):
    if 'username' not in session:
        flash("Please log in to book a room.")
        return redirect(url_for('login', next=request.path))

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM rooms WHERE id = %s", (room_id,))
    room = cursor.fetchone()
    if not room:
        flash("Room not found.")
        return redirect(url_for('home'))

    if request.method == 'POST':
        name = request.form['name']
        city = request.form['city']
        contact = request.form['contact']
        check_in = request.form['check_in']
        check_out = request.form['check_out']

        # Validate dates
        try:
            check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
            check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()
            if check_in_date >= check_out_date:
                flash("Check-out date must be after check-in date.")
                return redirect(request.url)
        except ValueError:
            flash("Invalid date format.")
            return redirect(request.url)

        user_id = get_user_id(session['username'])

        # Check for overlapping bookings for the same room
        cursor.execute("""
            SELECT * FROM bookings WHERE room_id = %s AND
            NOT (check_out <= %s OR check_in >= %s)
            """, (room_id, check_in, check_out))
        overlap = cursor.fetchone()
        if overlap:
            flash("Room is already booked for the selected dates. Please choose different dates.")
            return redirect(request.url)

        # Insert booking
        cursor.execute("""
            INSERT INTO bookings (user_id, room_id, name, city, contact, check_in, check_out)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (user_id, room_id, name, city, contact, check_in, check_out))
        mysql.connection.commit()
        cursor.close()
        flash("Room booked successfully!")
        return redirect(url_for('home'))

    cursor.close()
    room_data = {
        'id': room[0],
        'name': room[1],
        'description': room[2],
        'price': room[3],
        'image': room[4]
    }
    return render_template('book_room.html', room=room_data)

@app.route('/cancel_booking/<int:booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    if 'username' not in session:
        flash("Please log in to cancel a booking.")
        return redirect(url_for('login', next=request.path))

    cursor = mysql.connection.cursor()

    # Get user id from session username
    cursor.execute("SELECT id FROM users WHERE username = %s", (session['username'],))
    user = cursor.fetchone()
    if not user:
        flash("User not found.")
        return redirect(url_for('bookings'))
    user_id = user[0]

    # Check if the booking belongs to the logged-in user
    cursor.execute("SELECT * FROM bookings WHERE id = %s AND user_id = %s", (booking_id, user_id))
    booking = cursor.fetchone()
    if not booking:
        flash("Booking not found or unauthorized action.")
        cursor.close()
        return redirect(url_for('bookings'))

    # Delete the booking
    cursor.execute("DELETE FROM bookings WHERE id = %s", (booking_id,))
    mysql.connection.commit()
    cursor.close()

    flash("Booking canceled successfully.")
    return redirect(url_for('bookings'))


# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' in session:
        flash("You are already logged in.")
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash("Username already exists. Please choose another.")
            cursor.close()
            return redirect(url_for('register'))

        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        mysql.connection.commit()
        cursor.close()
        flash("Registration successful! Please log in.")
        return redirect(url_for('login'))

    return render_template('register.html')


# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        next_url = request.form.get('next', '/')

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        cursor.close()

        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]

            # Handle #rooms and book_room redirect logic
            if next_url == '/#rooms':
                return redirect(url_for('home') + '#rooms')
            elif next_url.startswith('/book_room/'):
                return redirect(next_url)
            else:
                return redirect('/')
        else:
            error = 'Invalid username or password'
            return render_template('login.html', error=error, next=next_url)
    else:
        next_url = request.args.get('next', '/')
        return render_template('login.html', next=next_url)



# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("You have been logged out.")
    return redirect(url_for('home'))

# Bookings page - only accessible if logged in
@app.route('/bookings')
def bookings():
    if 'username' not in session:
        flash("Please log in to view your bookings.")
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    # Get user_id from username
    cursor.execute("SELECT id FROM users WHERE username = %s", (session['username'],))
    user = cursor.fetchone()
    if not user:
        flash("User not found.")
        return redirect(url_for('home'))

    user_id = user[0]
    # Fetch bookings for this user, including booking id for cancel button
    cursor.execute("""
    SELECT b.id, r.name, r.price, b.check_in, b.check_out
    FROM bookings b
    JOIN rooms r ON b.room_id = r.id
    WHERE b.user_id = %s
    ORDER BY b.check_in DESC
    """, (user_id,))

    bookings_data = cursor.fetchall()
    cursor.close()

    bookings = []
    for row in bookings_data:
        booking_id = row[0]
        room_name = row[1]
        room_price = row[2]
        check_in = row[3]
        check_out = row[4]
        num_days = (check_out - check_in).days
        total_price = room_price * num_days

        bookings.append({
            'id': booking_id,
            'room_name': room_name,
            'check_in': check_in,
            'check_out': check_out,
            'price': room_price,
            'days': num_days,
            'total_price': total_price
        })


    return render_template('bookings.html', bookings=bookings, username=session['username'])
   
   



# Static pages
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/rooms')
def rooms():
    return render_template('rooms.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)