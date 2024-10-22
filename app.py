from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'clave_secreta'

# Inicializar la lista de inscritos en session
@app.route("/", methods=["GET", "POST"])
def index():
    if "inscritos" not in session:
        session["inscritos"] = []

    if request.method == "POST":
        nuevo_inscrito = {
            "fecha": request.form["fecha"],
            "nombre": request.form["nombre"],
            "apellidos": request.form["apellidos"],
            "turno": request.form["turno"],
            "seminarios": request.form.getlist("seminarios")
        }
        session["inscritos"].append(nuevo_inscrito)
        session.modified = True
        return redirect(url_for("lista_inscritos"))

    return render_template("registro.html")


@app.route("/lista", methods=["GET"])
def lista_inscritos():
    inscritos = session.get("inscritos", [])
    # Asigna un índice a cada inscrito
    inscritos_con_indices = [(i, inscrito) for i, inscrito in enumerate(inscritos)]
    return render_template("lista.html", inscritos=inscritos_con_indices)


@app.route("/eliminar/<int:index>", methods=["POST"])
def eliminar_inscrito(index):
    if "inscritos" in session:
        inscritos = session["inscritos"]
        if 0 <= index < len(inscritos):
            del inscritos[index]
            session.modified = True
    return redirect(url_for("lista_inscritos"))


@app.route("/editar/<int:index>", methods=["GET", "POST"])
def editar_inscrito(index):
    if "inscritos" in session:
        inscritos = session["inscritos"]
        if 0 <= index < len(inscritos):
            if request.method == "POST":
                inscritos[index] = {
                    "fecha": request.form["fecha"],
                    "nombre": request.form["nombre"],
                    "apellidos": request.form["apellidos"],
                    "turno": request.form["turno"],
                    "seminarios": request.form.getlist("seminarios")
                }
                session.modified = True
                return redirect(url_for("lista_inscritos"))
            return render_template("editar.html", index=index, inscrito=inscritos[index])
    return redirect(url_for("lista_inscritos"))


if __name__ == "__main__":
    app.run(debug=True)
