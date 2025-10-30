from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'rahasia123'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskmysql'
mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('inpEmail')
        passwd = request.form.get('inpPass')

        if email and passwd:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, passwd))
            result = cur.fetchone()
            cur.close()

            if result:
                session['is_logged_in'] = True
                session['username'] = result[1]
                return redirect(url_for('home'))
            else:
                error = "Email atau password salah!"
                return render_template('login.html', error=error)
        else:
            error = "Harap isi semua kolom!"
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/home')
def home():
    if 'is_logged_in' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users")
        data = cur.fetchall()
        cur.close()
        return render_template('home.html', users=data, username=session['username'])
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
