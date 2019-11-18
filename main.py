
import random
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

    sejna_vrednost = str(uuid.uuid4())

    uporabnik = db.query(Uporabnik).filter_by(sejna_vrednost=sejna_vrednost).first()
    if not uporabnik:
        uporabnik = Uporabnik(ime=ime, sejna_vrednost=sejna_vrednost)
    else:
        uporabnik.sejna_vrednost = sejna_vrednost

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



# main + TAB je spodnja vrstica (komanda da program teče!)
if __name__ == '__main__':
#    app.run()

# izpise v brskalniku napake debug=True
    app.run(debug=True)
