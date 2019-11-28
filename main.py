import hashlib
import random
import requests
import json
import uuid
# import Flask knjižnico
from flask import Flask, render_template, request, redirect, make_response
from modeli import Komentar, db, Uporabnik

# kliče glavno datoteko
app = Flask(__name__)
db.create_all()

# pot za prvo stran
@app.route("/")
def prva_stran():
    sejna_vrednost = request.cookies.get("sejna_vrednost")

    uporabnik = db.query(Uporabnik).filter_by(sejna_vrednost=sejna_vrednost).first()
    if uporabnik:
        ime = uporabnik.ime
    else:
        ime = None

    # Preberemo vse komentarje
    komentarji = db.query(Komentar).all()

    return render_template("prva_stran.html", ime=ime, komentarji=komentarji)




@app.route("/poslji-sporocilo", methods=["post"])
def poslji_sporocilo():
    zadeva = request.form.get("zadeva")
    sporocilo = request.form.get("sporocilo")

    # tukaj bi shranili te spremenljivke v bazo.

#    print ("zadeva je: " + zadeva)
#    print ("sporočilo je: " + sporocilo)
#    return "Hvala za poslano zadevo: " + zadeva

# spodaj zadeva=zadeva prva beseda je povezana z html >>vsebino ABC<<
#    return render_template("sporocilo_poslano.html", abc=zadeva)
    return render_template("sporocilo_poslano.html", zadeva=zadeva)

@app.route("/prijava", methods=["POST"])
def prijava():
    ime = request.form.get("ime")
    originalno_geslo = request.form.get("geslo")
    geslo = hashlib.sha256(originalno_geslo.encode()).hexdigest()

    sejna_vrednost = str(uuid.uuid4())

    # Geslo je potrebno šifrirati!

    uporabnik = db.query(Uporabnik).filter_by(ime=ime).first()
    if not uporabnik:
        uporabnik = Uporabnik(ime=ime, email="", geslo=geslo, sejna_vrednost=sejna_vrednost)
    else:
        if uporabnik.je_blokiran:
            return "Uporaba blokiran, prijava ni mogoča"

        if geslo == uporabnik.geslo:
            uporabnik.sejna_vrednost = sejna_vrednost
        else:
            return "Napačno geslo"

    db.add(uporabnik)
    db.commit()




    odgovor = make_response(redirect("/"))
    odgovor.set_cookie("sejna_vrednost", sejna_vrednost)
    return odgovor
#1    return redirect("https://www.smartninja.org/student/forum/course/5766390329901056/topic/5734963441827840")
#1    return "Testni izpis prijave"

@app.route("/komentar", methods=["POST"])
def poslji_komentar():
    vsebina_komentarja = request.form.get("vsebina")

    sejna_vrednost = request.cookies.get("sejna_vrednost")
    uporabnik = db.query(Uporabnik).filter_by(sejna_vrednost=sejna_vrednost).first()

    komentar = Komentar(
        avtor=uporabnik.ime,
        vsebina=vsebina_komentarja
    )
    db.add(komentar)

    db.commit()

    return redirect("/")


# pot do datoteke kontaktov
@app.route("/kontakt")
def kontakt():
    emaili = ["ime@example.com", "ime@gmail.com", "tretji@email.si"]
    return render_template("kontakt.html", emaili=emaili)

# pot do datoteke o meni
@app.route("/o meni")
def o_meni():
    return render_template("o meni.html")

@app.route("/skrito-stevilo")
def skrito_stevilo():
    odgovor = make_response(render_template("skrito_stevilo.html"))

    if not request.cookies.get("skritoSteviloPiskot"):
        stevilo = str(random.randint(1, 20))
        odgovor.set_cookie("skritoSteviloPiskot", stevilo)

    return odgovor

@app.route("/poslji-skrito-stevilo", methods=["POST"])
def poslji_skrito_stevilo():
    skrito_stevilo = request.cookies.get("skritoSteviloPiskot")
    vpisano_stevilo = request.form.get("stevilo")

    if skrito_stevilo == vpisano_stevilo:
        return "PRAVILNO"
    else:
        return "NI PRAVILNO"

@app.route("/profil")
def moj_profil():
    sejna_vrednost = request.cookies.get("sejna_vrednost")
    uporabnik = db.query(Uporabnik).filter_by(sejna_vrednost=sejna_vrednost).first()

    if not uporabnik:
        return "Napačna seja"

    return render_template("profil.html", uporabnik=uporabnik)

@app.route("/profil/uredi", methods=["GET", "POST"])
def uredi_profil():
    sejna_vrednost = request.cookies.get("sejna_vrednost")
    uporabnik = db.query(Uporabnik).filter_by(sejna_vrednost=sejna_vrednost).first()

    if not uporabnik:
        return "Napačna seja"

    if request.method == "GET":
        return render_template("uredi_profil.html", uporabnik=uporabnik)
    elif request.method == "POST":
        uporabnik.ime = request.form.get("ime")
        uporabnik.email = request.form.get("email")

        db.add(uporabnik)
        db.commit()

        return redirect("/profil")

@app.route("/profil/izbrisi", methods=["GET", "POST"])
def izbrisi_profil():
    sejna_vrednost = request.cookies.get("sejna_vrednost")
    uporabnik = db.query(Uporabnik).filter_by(sejna_vrednost=sejna_vrednost).first()

    if not uporabnik:
        return "Napačna seja"

    if request.method == "GET":
        return render_template("izbrisi_profil.html")
    elif request.method == "POST":
        db.delete(uporabnik)
        db.commit()

        odgovor = make_response(redirect("/"))
        odgovor.set_cookie("sejna_vrednost", expires=0)
        return odgovor

@app.route("/uporabniki")
def uporabniki():
    users = db.query(Uporabnik).all()
    return render_template("uporabniki.html", uporabniki=users)

# <uporabnik_id> to kaže na cifro ID uporabnika to je dinamična 'stran'
@app.route("/uporabniki/<uporabnik_id>", methods=["GET", "POST"])
def prikaz_uporabnika(uporabnik_id):
    uporabnik = db.query(Uporabnik).filter_by(id=uporabnik_id).first()


    if request.method == "POST":

        blokiran = False
        if request.form.get("je_blokiran") == "on":
            blokiran = True
        uporabnik.je_blokiran = blokiran
        db.add(uporabnik)
        db.commit()

    return render_template("prikaz_uporabnika.html", uporabnik=uporabnik)

@app.route("/vreme")
def vreme():
    mesto = "Lendava"
    odgovor_geo = json.loads(requests.get("https://geocode.xyz/" + mesto + "?json=1").text)
    lon = odgovor_geo["longt"]
    lat = odgovor_geo["latt"]

# glej alternativne načine pri ROKU! glede url in spremenljivke lat in lon (zgoraj) !!!
    url = "https://opendata.si/vreme/report/?lat=" + lat + "&lon=" + lon
    odgovor = json.loads(requests.get(url).text)

    dez = odgovor["forecast"]["data"][0]["rain"]

    return render_template("vreme.html", vreme=dez)


if __name__ == '__main__':
    app.run(debug=True)
