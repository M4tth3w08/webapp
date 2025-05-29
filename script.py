from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import calendar

app = Flask(__name__)
giorni_esercizi = {}

@app.route("/", methods=["GET", "POST"])
def index():
    today = datetime.today()

    # Controllo dei parametri mese e anno con valori di default e sanitizzazione
    try:
        anno = int(request.args.get("anno", today.year))
        mese = int(request.args.get("mese", today.month))
        if mese < 1:
            mese = 1
        elif mese > 12:
            mese = 12
    except ValueError:
        anno = today.year
        mese = today.month

    mese_nome = calendar.month_name[mese]
    giorno_corrente = today.day if (anno == today.year and mese == today.month) else None
    _, num_giorni = calendar.monthrange(anno, mese)

    selected_data = request.form.get("selected_date") if request.method == "POST" else None

    if not selected_data and anno == today.year and mese == today.month:
        selected_data = today.strftime("%Y-%m-%d")

    esercizi_selezionati = giorni_esercizi.get(selected_data, [])

    mese_prec = mese - 1 if mese > 1 else 12
    anno_prec = anno if mese > 1 else anno - 1
    mese_succ = mese + 1 if mese < 12 else 1
    anno_succ = anno if mese < 12 else anno + 1

    return render_template("index.html",
                           anno=anno,
                           mese=mese,
                           mese_nome=mese_nome,
                           giorni=num_giorni,
                           esercizi=giorni_esercizi,
                           giorno_corrente=giorno_corrente,
                           selected_data=selected_data,
                           esercizi_selezionati=esercizi_selezionati,
                           mese_prec=mese_prec,
                           anno_prec=anno_prec,
                           mese_succ=mese_succ,
                           anno_succ=anno_succ,
                           mese_corrente=today.month,
                           anno_corrente=today.year)

@app.route("/giorno/<data>", methods=["GET", "POST"])
def giorno(data):
    if request.method == "POST":
        if "delete_index" in request.form:
            idx = int(request.form["delete_index"])
            if data in giorni_esercizi and 0 <= idx < len(giorni_esercizi[data]):
                giorni_esercizi[data].pop(idx)
                if not giorni_esercizi[data]:
                    del giorni_esercizi[data]
        else:
            nome = request.form.get("nome", "").strip()
            serie = request.form.get("serie", "").strip()
            ripetizioni = request.form.get("ripetizioni", "").strip()
            note = request.form.get("note", "").strip()

            if nome and serie and ripetizioni:
                esercizio = {
                    "nome": nome,
                    "serie": serie,
                    "ripetizioni": ripetizioni,
                    "note": note
                }

                giorni_esercizi.setdefault(data, []).append(esercizio)

        return redirect(url_for("giorno", data=data))

    esercizi = giorni_esercizi.get(data, [])
    giorno_numero = int(data.split("-")[2])
    return render_template("esercizio.html", data=data, giorno=giorno_numero, esercizi=esercizi)

if __name__ == "__main__":
    app.run(debug=True)