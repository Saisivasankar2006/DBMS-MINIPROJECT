from flask import Flask, render_template, redirect, request, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'tamil'

# MySQL configuration for Pet Shop Management
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345678'  # Replace with your actual password
app.config['MYSQL_DB'] = 'pet_shop_db'  # Updated to pet_shop_db
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.htm')

@app.route('/pets')  # Changed route from '/doctor' to '/pets'
def pets():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM petdetails")  # Updated table name
    pet_info = cur.fetchall()
    cur.close()
    return render_template('pets.htm', pets=pet_info)  # Updated template name

@app.route('/search', methods=['POST', 'GET'])
def search():
    search_results = []
    if request.method == "POST":
        search_term = request.form.get('petid')  # Use .get() to avoid KeyError
        cur = mysql.connection.cursor()
        query = "SELECT * FROM petdetails WHERE id LIKE %s"  # Updated table name
        cur.execute(query, ('%' + search_term + '%',))
        search_results = cur.fetchall()  # Use fetchall() to get all results
        cur.close()
        return render_template('pets.htm', pets=search_results)  # Updated template name

@app.route('/insert', methods=['POST'])
def insert():
    if request.method == "POST":
        id_data = request.form.get('petid')  # Corrected to use .get()
        name = request.form.get('name')         # Corrected to use .get()
        breed = request.form.get('breed')       # Changed from 'specialty' to 'breed'
        age = request.form.get('age')           # Added age field
        owner_email = request.form.get('owner_email')  # Added owner_email field

        # Check if all fields are provided
        if not all([id_data, name, breed, age, owner_email]):
            return render_template('pets.htm', error="All fields are required.")  # Updated error message

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO petdetails (id, name, breed, age, owner_email) VALUES (%s, %s, %s, %s, %s)",
                    (id_data, name, breed, age, owner_email))  # Insert relevant pet data
        mysql.connection.commit()
        return redirect(url_for('pets'))  # Redirect to updated pets route

@app.route('/delete/<string:id_data>', methods=['GET'])
def delete(id_data):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM petdetails WHERE id=%s", (id_data,))  # Updated table name
    mysql.connection.commit()
    return redirect(url_for('pets'))  # Redirect to updated pets route

@app.route('/update/<string:id_data>', methods=['POST', 'GET'])
def update(id_data):
    if request.method == 'POST':
        name = request.form.get('name')
        breed = request.form.get('breed')
        age = request.form.get('age')
        owner_email = request.form.get('owner_email')

        # Check if all fields are provided
        if not all([name, breed, age, owner_email]):
            return render_template('pets.htm', error="All fields are required for update.")  # Updated error message

        cur = mysql.connection.cursor()
        cur.execute("UPDATE petdetails SET name=%s, breed=%s, age=%s, owner_email=%s WHERE id=%s", 
                    (name, breed, age, owner_email, id_data))  # Update relevant pet data
        mysql.connection.commit()
        return redirect(url_for('pets'))  # Redirect to updated pets route

    # Fetch pet details for updating the form
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM petdetails WHERE id=%s", (id_data,))
    pet = cur.fetchone()
    cur.close()
    return render_template('update_pet.htm', pet=pet)  # New template for updating a pet

if __name__ == "__main__":
    app.run(debug=True)
