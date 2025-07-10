from flask import Flask, render_template, request, redirect, url_for
import sqlite3



def get_db_connection():
    conn = sqlite3.connect('alumnos.db')
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)

app.route("/", methods=["GET"])
def index():
    return render_template("base.html")

@app.route("/home", methods=["GET"])
def home():
    return render_template("home.html")

@app.route("/post", methods=["GET"])
def get_all_post():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM alumnos;').fetchall()
    return render_template("post/post_list.html", posts=posts)

@app.route("/post/<int:post_id>", methods=["GET"])
def get_one_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM alumnos WHERE id = ?', (post_id,)).fetchone()
    print(post)
    if post is None:
        abort(404)
    return render_template("post/post.html", post=post)

@app.route('/post/create', methods=['GET', 'POST'])
def create_one_post():
    if request.method == "GET":
        return render_template("post/create.html")
    if request.method == "POST":
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        aprobado = request.form["aprobado"]
        nota = request.form["nota"]
        fecha = request.form["fecha"]
        conn = get_db_connection()
        conn.execute('INSERT INTO alumnos (nombre, apellido, aprobado, nota, fecha) VALUES (?, ?, ?, ?, ?)', (nombre, apellido, aprobado, nota, fecha))
        conn.commit()
        conn.close()
        return redirect(url_for('get_all_post'))


@app.route('/post/update/<int:post_id>', methods=['GET', 'POST'])
def update_one_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM alumnos WHERE id = ?', (post_id,)).fetchone()
    
    if request.method == "GET":
        return render_template("post/update.html", post=post)
    if request.method == "POST":
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        aprobado = request.form["aprobado"]
        conn = get_db_connection()
        conn.execute('UPDATE alumnos SET nombre= ?, apellido = ?,  aprobado = ?  WHERE id = ?', (nombre, apellido, aprobado , post_id))
        conn.commit()
        conn.close()
        return redirect(url_for('get_all_post'))

@app.route('/post/delete/<int:post_id>', methods=['POST'])
def delete_one_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM alumno WHERE id = ?', (post_id,)).fetchone()

    if post is None:
        conn.close()
        abort(404)

    conn.execute('DELETE FROM alumno WHERE id = ?', (post_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('get_all_post'))




if __name__ == '__main__':
    app.run(debug=True)