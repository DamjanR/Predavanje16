# import Flask knjižnico
from flask import Flask, render_template, request

# kliče glavno datoteko
app = Flask(__name__)

# pot za prvo stran
@app.route("/")
def prva_stran():
    return render_template("prva_stran.html")

@app.route("/poslji-sporocilo", methods=["post"])
def poslji_sporocilo():
    zadeva = request.form.get("zadeva")
    sporocilo = request.form.get("sporocilo")

    # tukaj bi shranili te spremenljivke v bazo.

#    print ("zadeva je: " + zadeva)
#    print ("sporočilo je: " + sporocilo)
#    return "Hvala za poslano zadevo: " + zadeva
    return render_template("sporocilo_poslano.html", zadeva=zadeva)


# pot do datoteke kontaktov
@app.route("/kontakt")
def kontakt():
    emaili = ["ime@example.com", "ime@gmail.com", "tretji@email.si"]
    return render_template("kontakt.html", emaili=emaili)

# pot do datoteke o meni
@app.route("/o meni")
def o_meni():
    return render_template("o meni.html")


# main + TAB je spodnja vrstica (komanda da program teče!)
if __name__ == '__main__':
    app.run()
