# import Flask knjižnico
from flask import Flask, render_template, request, redirect, make_response

# kliče glavno datoteko
app = Flask(__name__)

# pot za prvo stran
@app.route("/")
def prva_stran():
    ime = request.cookies.get("ime")

    return render_template("prva_stran.html", ime=ime)

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
    odgovor = make_response(redirect("/"))
#1    print("prijava")
    odgovor.set_cookie("ime", ime)
    return odgovor
#1    return redirect("https://www.smartninja.org/student/forum/course/5766390329901056/topic/5734963441827840")
#1    return "Testni izpis prijave"


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
#    app.run()

# izpise v brskalniku napake debug=True
    app.run(debug=True)
