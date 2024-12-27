from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

# Configuración de la clave secreta para sesiones
app.secret_key = 'tu_clave_secreta'  # Cambia esto por una clave secreta más segura

# Lista de usuarios y contraseñas
users = {
    "admin": "admin123",
    "usuario1": "clave123",
    "carlos": "123"
}

# Definimos las preguntas por área
areas = {
    "literatura": [
        {"question": "¿Quién escribió 'Cien años de soledad'?", "answer": "Gabriel García Márquez"},
        {"question": "¿En qué año se publicó 'Don Quijote de la Mancha'?", "answer": "1605"},
        {"question": "¿Quién es el autor de 'Matar a un ruiseñor'?", "answer": "Harper Lee"}
    ],
    "psicologia": [
        {"question": "¿Quién es el padre del psicoanálisis?", "answer": "Sigmund Freud"},
        {"question": "¿Qué es el condicionamiento clásico?", "answer": "Es un tipo de aprendizaje en el que un estímulo neutro llega a provocar una respuesta condicionada."},
        {"question": "¿Qué es la teoría del apego?", "answer": "Es una teoría psicológica que describe la dinámica de las relaciones a largo plazo entre los humanos."}
    ],
    "derecho": [
        {"question": "¿Qué es el derecho penal?", "answer": "Es una rama del derecho que se ocupa de las conductas ilícitas y las sanciones aplicables a los infractores."},
        {"question": "¿Cuál es la principal fuente del derecho en la mayoría de los países?", "answer": "La Constitución y las leyes promulgadas por el legislador."},
        {"question": "¿Qué es el derecho civil?", "answer": "Es una rama del derecho privado que regula las relaciones entre los particulares."}
    ]
}

# Página de login
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if users.get(username) == password:
            session['user'] = username  # Guardamos al usuario en la sesión
            return redirect(url_for('areas'))  # Redirigimos a la página de selección de áreas
        else:
            return render_template('index.html', error="Credenciales incorrectas.")
    return render_template('index.html', error=None)

# Página de selección de áreas
@app.route("/areas")
def areas():
    if 'user' not in session:
        return redirect(url_for('login'))  # Si no está logueado, redirigir al login
    
    return render_template('areas.html')  # Mostrar las opciones de áreas

# Página de preguntas por área
@app.route("/preguntas/<area>")
def preguntas(area):
    if 'user' not in session:
        return redirect(url_for('login'))  # Si no está logueado, redirigir al login
    
    if area not in areas:
        return redirect(url_for('areas'))  # Si el área no existe, redirigir a la selección de áreas
    
    # Obtener las preguntas y respuestas del área seleccionada
    area_questions = areas[area]
    
    # Guardar el índice de la pregunta actual en la sesión
    session['area'] = area
    session['question_index'] = 0  # Empezamos con la primera pregunta

    return render_template('preguntas.html', area=area, questions=area_questions[session['question_index']])

# Página de cambiar pregunta
@app.route("/cambiar_pregunta", methods=["POST"])
def cambiar_pregunta():
    if 'user' not in session:
        return redirect(url_for('login'))  # Si no está logueado, redirigir al login

    area = session.get('area')
    question_index = session.get('question_index')

    area_questions = areas[area]

    # Avanzar al siguiente índice o volver al inicio si ya se alcanzó el final
    question_index = (question_index + 1) % len(area_questions)
    session['question_index'] = question_index

    return redirect(url_for('preguntas', area=area))  # Redirigir a la página de preguntas con el nuevo índice

# Cerrar sesión
@app.route("/logout")
def logout():
    session.pop('user', None)  # Elimina el usuario de la sesión
    session.pop('area', None)  # Elimina el área de la sesión
    session.pop('question_index', None)  # Elimina el índice de la pregunta
    return redirect(url_for('login'))  # Redirige al login después de cerrar sesión

if __name__ == "__main__":
    app.run(debug=True)  # Ejecuta en modo de depuración
