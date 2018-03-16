from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
app = Flask(__name__)
app.secret_key = 'SuperSecretKey'
mysql = MySQLConnector(app,'usersdb2')


@app.route('/')
def root():
    return redirect('/users')


@app.route('/users')
def index():
    query = "SELECT id, CONCAT_WS(' ', first_name, last_name) AS name, email, "
    query += "  DATE_FORMAT(created_at, '%M %D, %Y %H:%i:%s') AS time, "
    query += "  DATE_FORMAT(updated_at, '%M %D, %Y %H:%i:%s') AS updated_time "
    query += "FROM users"
    data = mysql.query_db(query)
    return render_template('users.html', all_users=data)


@app.route('/users/new')
def new():
    return render_template('user_new.html')


@app.route('/users/<id>/edit')
def edit(id):
    return render_template('user_edit.html', user_id=id)


@app.route('/users/<id>')
def show(id):
    query = "SELECT id, CONCAT_WS(' ', first_name, last_name) AS name, email, "
    query += "  DATE_FORMAT(created_at, '%M %D, %Y %H:%i:%s') AS time "
    query += "FROM users WHERE id = {}".format(id)
    data = mysql.query_db(query)
    return render_template('user.html', user=data[0])


@app.route('/users/create', methods=['POST'])
def create():
    query = "INSERT INTO users (first_name, last_name, email, created_at, updated_at) "
    query += "VALUES (:first_name, :last_name, :email, NOW(), NOW()) "
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email']
    }
    id = mysql.query_db(query, data)
    return redirect('/users/{}'.format(id))


@app.route('/users/<id>/destroy')
def destory(id):
    query = "DELETE FROM users WHERE id = {}".format(id)
    mysql.query_db(query)
    return redirect('/users')


@app.route('/users/<id>', methods=['POST'])
def update(id):
    query = "UPDATE users SET "
    query += "first_name = '{}', ".format(request.form['first_name'])
    query += "last_name = '{}', ".format(request.form['last_name'])
    query += "email = '{}', ".format(request.form['email'])
    query += "updated_at = NOW() "
    query += "WHERE id = {}".format(id)

    mysql.query_db(query)
    return redirect('/users/{}'.format(id))


app.run(debug=True)



