# Import Flask framework and tools for rendering pages, handling requests and also sessions
from flask import Flask, render_template, request, session, redirect

# Import SQLite for database connection
import sqlite3

# Import password hashing tools for security
from werkzeug.security import generate_password_hash, check_password_hash

# Create the Flask application
app = Flask(__name__)

# Secret key will be required for session security
app.secret_key = "secure_secret_key"

# Homepage route (this route loads the homepage of the system)
@app.route("/")
def home():
    return render_template("index.html")

# Registration page route (this route allows users to register an account)
@app.route("/register", methods=["GET", "POST"])
def register():

# If the registration form is submitted
    if request.method == "POST":

# Get the form data from the HTML form
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

# Hash the password before storing it
        hashed_password = generate_password_hash(password)

# Connect to SQlite database
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

# Insert the new user into the database
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, hashed_password)
        )

# Save changes and close the connection
        conn.commit()
        conn.close()

        return "User registered successfully!"

    return render_template("register.html")
    

# User login route (this route handles authentication)
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

# Get login details from form
        email = request.form["email"]
        password = request.form["password"]

# Connect to database
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

# Find user by email
        cursor.execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        )

        user = cursor.fetchone()

        conn.close()

# If user exists
        if user:

            stored_password = user[3]

# Verify hashed password
            if check_password_hash(stored_password, password):

# Create session (user is now logged in)
                session["user"] = user[1]

                return render_template("dashboard.html")

            else:
                return "Invalid password"

        else:
            return "User not found"

    return render_template("login.html")

# Dashboard route (only accessible when logged in)
@app.route('/dashboard')
def dashboard():
    if "user" not in session:
        return redirect('/login')

    return render_template("dashboard.html")
    
# Patient management route ( this allows adding of patient records)
@app.route("/patients", methods=["GET", "POST"])
def patients():

# Check if user is logged in
    if "user" not in session:
        return redirect('/login')
    
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

# If user submits a new patient
    if request.method == "POST":

        name = request.form["name"]
        age = request.form["age"]
        diagnosis = request.form["diagnosis"]
        treatment = request.form["treatment"]

        cursor.execute(
            "INSERT INTO patients (name, age, diagnosis, treatment) VALUES (?, ?, ?, ?)",
            (name, age, diagnosis, treatment)
        )

        conn.commit()

# Fetch all patients from database
    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()

    conn.close()

    return render_template("patients.html", patients=patients)

# Edit patient information
@app.route('/edit_patient/<int:id>', methods=['GET', 'POST'])
def edit_patient(id):

    # Check login
    if "user" not in session:
        return redirect('/login')

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    if request.method == 'POST':

        # Get form data
        name = request.form['name']
        age = request.form['age']
        diagnosis = request.form['diagnosis']
        treatment = request.form['treatment']

        # Validation (ONLY here)
        if not name or not age or not diagnosis or not treatment:
            return "Please fill all fields"

        # Update database
        cursor.execute(
            "UPDATE patients SET name=?, age=?, diagnosis=?, treatment=? WHERE id=?",
            (name, age, diagnosis, treatment, id)
        )

        conn.commit()
        conn.close()

        return redirect('/patients')

    # Get request (load existing data)
    cursor.execute("SELECT * FROM patients WHERE id=?", (id,))
    patient = cursor.fetchone()

    conn.close()

    return render_template('edit_patient.html', patient=patient)

# Connect to database
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

# Insert patient record
    cursor.execute(
            "INSERT INTO patients (name, age, diagnosis, treatment) VALUES (?, ?, ?, ?)",
            (name, age, diagnosis, treatment)
        )

    conn.commit()
    conn.close()

    return "Patient added successfully!"

    return render_template("patients.html")


# Delete the patient route
@app.route("/delete_patient/<int:patient_id>")
def delete_patient(patient_id):

    if "user" not in session:
        return redirect('/login')

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM patients WHERE id=?",
        (patient_id,)
    )

    conn.commit()
    conn.close()

    return redirect("/patients")

# Logout route ( this clears the logged in session and clears the user out)
@app.route("/logout")
def logout():

    # If user is not logged in, send to login page
    if "user" not in session:
        return redirect('/login')

    # Remove user session
    session.pop("user", None)

    # Redirect to login page after logout
    return redirect('/login')

# Run the application (this will start thee Flask development server)
if __name__ == "__main__":
    app.run(debug=True)

   