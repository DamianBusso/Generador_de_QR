from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Crear la base de datos si no existe
def init_db():
    conn = sqlite3.connect('database.db')
    conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT)')
    conn.close()

# Ruta para mostrar el formulario de registro
@app.route('/')
def index():
    return render_template('register.html')

# Ruta para manejar el registro
@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email']
    
    # Guardar los datos en la base de datos
    conn = sqlite3.connect('database.db')
    conn.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
    conn.commit()
    conn.close()
    
    return redirect('/users')

# Ruta para mostrar la lista de usuarios
@app.route('/users')
def users():
    conn = sqlite3.connect('database.db')
    cursor = conn.execute('SELECT id, name, email FROM users')  # Selecciona también el ID
    users = cursor.fetchall()
    conn.close()
    
    return render_template('users.html', users=users)

# **Nueva ruta para eliminar un usuario** 
@app.route('/delete/<int:id>', methods=['POST'])
def delete_user(id):
    conn = sqlite3.connect('database.db')
    conn.execute('DELETE FROM users WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    return redirect('/users')

if __name__ == '__main__':
    init_db()  # Inicializar la base de datos
    app.run(debug=True)

