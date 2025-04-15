import http.server
import json
import mysql.connector
import hashlib
import re
from http.cookies import SimpleCookie
from urllib.parse import urlparse, parse_qs

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Tej@shwini05',
    'database': 'Desi'
}

def connect_to_database():
    """Connects to the MySQL database."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except mysql.connector.Error as error:
        print(f"Error connecting to MySQL: {error}")
        return None

def close_database_connection(connection, cursor=None):
    """Closes the database connection and cursor."""
    if cursor:
        cursor.close()
    if connection and connection.is_connected():
        connection.close()

def hash_the_password(password):
    """Hashes the password using SHA256 for security."""
    return hashlib.sha256(password.encode()).hexdigest()

def handle_login(data, handler):
    """Handles user login requests."""
    username = data.get('username')
    password = data.get('password')
    hashed_password = hash_the_password(password)

    db_connection = connect_to_database()
    cursor = None

    if not db_connection:
        return json.dumps({'success': False, 'message': 'Database connection failed.'}).encode('utf-8')

    try:
        cursor = db_connection.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, hashed_password))
        user_data = cursor.fetchone()

        if user_data:
            # Set a cookie to indicate successful login and redirect
            handler.send_response(302)
            handler.send_header('Location', '/')
            handler.send_header('Set-Cookie', 'logged_in=true; Path=/')
            handler.end_headers()
            return None  # No JSON response needed for redirect
        else:
            return json.dumps({'success': False, 'message': 'Invalid username or password.'}).encode('utf-8')
    except mysql.connector.Error as error:
        return json.dumps({'success': False, 'message': f'Database error: {error}'}).encode('utf-8')
    finally:
        close_database_connection(db_connection, cursor)

def handle_register(data, handler):
    """Handles user registration requests."""
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    phone = data.get('phone')

    # Server-side validation (matching client-side - keep this consistent)
    if not username.strip():
        return json.dumps({'success': False, 'message': 'Username cannot be empty.'}).encode('utf-8')
    if len(password) < 8:
        return json.dumps({'success': False, 'message': 'Password must be at least 8 characters long.'}).encode('utf-8')
    if not re.search(r'[A-Z]', password):
        return json.dumps({'success': False, 'message': 'Password must have an uppercase letter.'}).encode('utf-8')
    if not re.search(r'[a-z]', password):
        return json.dumps({'success': False, 'message': 'Password must have a lowercase letter.'}).encode('utf-8')
    if not re.search(r'[0-9]', password):
        return json.dumps({'success': False, 'message': 'Password must have a number.'}).encode('utf-8')
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return json.dumps({'success': False, 'message': 'Password must have a special character.'}).encode('utf-8')
    email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    if not re.match(email_regex, email):
        return json.dumps({'success': False, 'message': 'Invalid email format.'}).encode('utf-8')
    phone_regex = r'^(\+91[\-\s]?)?[6789]\d{9}$'
    if not re.match(phone_regex, phone):
        return json.dumps({'success': False, 'message': 'Invalid Indian phone number format.'}).encode('utf-8')

    hashed_password = hash_the_password(password)

    db_connection = connect_to_database()
    cursor = None

    if not db_connection:
        return json.dumps({'success': False, 'message': 'Database connection failed.'}).encode('utf-8')

    try:
        cursor = db_connection.cursor()
        query = "INSERT INTO users (username, password, email, phone) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (username, hashed_password, email, phone))
        db_connection.commit()

        # Set a cookie to indicate successful registration and redirect
        handler.send_response(302)
        handler.send_header('Location', '/')
        handler.send_header('Set-Cookie', 'logged_in=true; Path=/')
        handler.end_headers()
        return None  # No JSON response needed for redirect
    except mysql.connector.IntegrityError:
        return json.dumps({'success': False, 'message': 'Username or email already exists.'}).encode('utf-8')
    except mysql.connector.Error as error:
        return json.dumps({'success': False, 'message': f'Database error: {error}'}).encode('utf-8')
    finally:
        close_database_connection(db_connection, cursor)

class MyHandler(http.server.BaseHTTPRequestHandler):
    """Handles HTTP requests."""
    def do_POST(self):
        """Handles POST requests (login and registration)."""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        data = json.loads(post_data)

        if self.path == '/login':
            response = handle_login(data, self)
            if response:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(response)
        elif self.path == '/register':
            response = handle_register(data, self)
            if response:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(response)
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        """Handles GET requests (serving HTML files and checking login status)."""
        parsed_url = urlparse(self.path)
        path = parsed_url.path

        cookies = SimpleCookie(self.headers.get('Cookie'))
        logged_in = cookies.get('logged_in')

        file_paths = {
            '/': 'index.html',
            '/login': 'login.html',
            '/register': 'register.html',
            '/dishes.html': 'dishes.html',
        }

        file_path = file_paths.get(path)

        if path == '/':
            if logged_in:
                file_path = 'index.html'
            else:
                self.send_response(302)
                self.send_header('Location', '/login')
                self.end_headers()
                return

        elif path in ['/login', '/register']:
            if logged_in:
                self.send_response(302)
                self.send_header('Location', '/')
                self.end_headers()
                return
            else:
                file_path = file_paths.get(path)
        elif path == '/dishes.html':
            if not logged_in:
                self.send_response(302)
                self.send_header('Location', '/login')
                self.end_headers()
                return
            else:
                file_path = file_paths.get(path)

        if file_path:
            try:
                with open(file_path, 'rb') as file:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(file.read())
            except FileNotFoundError:
                self.send_response(404)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = http.server.HTTPServer(server_address, MyHandler)
    print('Server started on port 8000...')
    httpd.serve_forever()