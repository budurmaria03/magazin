from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_PORT'] = '3306'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'maria1234'
app.config['MYSQL_DB'] = 'magazin'

mysql = MySQL(app)


# vizualizare date din minim 3 tabele
@app.route('/products')
def products():
    cu = mysql.connection.cursor()
    cu.execute("SELECT * FROM Produse")
    products = cu.fetchall()
    #for product in products:
        #print(product)
    cu.close()
    return render_template('index.html', products=products)

@app.route('/categories')
def categories():
    cu = mysql.connection.cursor()
    cu.execute("SELECT * FROM Categorii")
    categories = cu.fetchall()
    #for category in categories:
        #print(category)
    cu.close()
    return render_template('index.html', categories=categories)

@app.route('/details')
def details():
    cu = mysql.connection.cursor()
    cu.execute("SELECT * FROM Detalii_comanda")
    details = cu.fetchall()
    #for detail in details:
        #print(detail)
    cu.close()
    return render_template('index.html', details=details)


# inserare, actualizare, ștergere a datelor, în minim 1 tabel
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        nume = request.form['Nume']
        pret = request.form['Pret']
        stoc = request.form['Stoc']
        grame = request.form['Gramaj']
        data_fabricatiei = request.form['Data_fabricatiei']
        data_expirarii = request.form['Data_expirarii']
        categorie = request.form['Categorie']
        cu = mysql.connection.cursor()
        cu.execute("INSERT INTO Produse (Nume, Pret, Stoc, Gramaj, Data_fabricatiei, Data_expirarii, Categorie) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                   (nume, pret, stoc, grame, data_fabricatiei, data_expirarii, categorie))
        mysql.connection.commit()
        cu.close()
        return redirect("/D:/ETTI/An%202/S2/Baze%20de%20Date/Laborator/Magazin%20Online/operatiiModificare1.html")
    #return render_template('createProdus.html')
    
@app.route('/add_category', methods=['GET', 'POST'])
def add_category():
    if request.method == 'POST':
        nume = request.form['Nume']
        cu = mysql.connection.cursor()
        cu.execute("INSERT INTO Categorii (Nume) VALUES (%s)",(nume))
        mysql.connection.commit()
        cu.close()
        return redirect("/D:/ETTI/An%202/S2/Baze%20de%20Date/Laborator/Magazin%20Online/operatiiModificare2.html")    
    #return render_template('createCategorie.html')

@app.route('/delete_product', methods=['POST'])
def delete_product():
    if request.method == 'POST':
        id_produs=request.form['Id.produs']
        cu = mysql.connection.cursor()
        cu.execute("DELETE FROM Produse WHERE Id_produs = %s", (id_produs))
        mysql.connection.commit()
        cu.close()
        return redirect("/D:/ETTI/An%202/S2/Baze%20de%20Date/Laborator/Magazin%20Online/operatiiModificare1.html")

@app.route('/delete_category', methods=['POST'])
def delete_category():
    if request.method == 'POST':
        id_categorie=request.form['Id.categorie']
        cu = mysql.connection.cursor()
        cu.execute("DELETE FROM Categorii WHERE Id_categorie = %s", (id_categorie))
        mysql.connection.commit()
        cu.close()
        return redirect("/D:/ETTI/An%202/S2/Baze%20de%20Date/Laborator/Magazin%20Online/operatiiModificare2.html")

@app.route('/update_product', methods=['GET', 'POST'])
def update_product():
    if request.method == 'POST':
        id_produs = request.form['Id_produs']
        nume = request.form['Nume']
        pret = request.form['Pret']
        stoc = request.form['Stoc']
        grame = request.form['Gramaj']
        data_fabricatiei = request.form['Data_fabricatiei']
        data_expirarii = request.form['Data_expirarii']
        categorie = request.form['Categorie']
        cu = mysql.connection.cursor()
        cu.execute("UPDATE Produse SET Nume=%s, Pret=%s, Stoc=%s, Gramaj=%s, Data_fabricatiei=%s, Data_expirarii=%s, Categorie=%s WHERE Id_produs = %s", (nume, pret, stoc, grame, data_fabricatiei, data_expirarii, categorie,id_produs))
        mysql.connection.commit()
        cu.close()
        return redirect("/D:/ETTI/An%202/S2/Baze%20de%20Date/Laborator/Magazin%20Online/operatiiModificare1.html")
    #return render_template('editProdus.html')

@app.route('/update_category/<int:id>', methods=['GET', 'POST'])
def update_category():
    if request.method == 'POST':
        nume = request.form['Nume']
        id_categorie=request.form['Id.categorie']
        cu = mysql.connection.cursor()
        cu.execute("UPDATE Categorii SET Nume = %s WHERE Id_categorie = %s", (nume, id_categorie))
        mysql.connection.commit()
        cu.close()
        return redirect("/D:/ETTI/An%202/S2/Baze%20de%20Date/Laborator/Magazin%20Online/operatiiModificare2.html")
    #return render_template('editCategorie.html')


# minim 5 interogări intra-tabel (în același tabel) (din care minim 3 cu clauze secundare)
@app.route('/query1', methods=['GET', 'POST'])
def query1():
    if request.method == 'POST':
        cu = mysql.connection.cursor()
        cu.execute("SELECT Nume, Pret FROM Produse WHERE Pret > 100")
        results1=cu.fetchall()
        cu.execute("SELECT Nume, Stoc FROM Produse WHERE Stoc < 20")
        results2=cu.fetchall()
        cu.execute("SELECT Nume, Pret, Stoc, Gramaj, Data_fabricatiei, Data_expirarii, Categorie FROM Produse ORDER BY Nume ASC")
        results3=cu.fetchall()
        cu.execute("SELECT * FROM Produse LIMIT 10")
        results4=cu.fetchall()
        cu.execute("SELECT Categorie, AVG(Pret) AS Pret_mediu, SUM(Stoc) AS Stoc_total FROM Produse GROUP BY Categorie HAVING SUM(Stoc) > 50")
        results5=cu.fetchall()
        cu.close()
        return render_template('interfata_interogare_1.html', results1=results1, results2=results2, results3=results3, results4=results4, results5=results5)
    

# minim 2 interogări inter-tabele (2 sau mai multe tabele)
@app.route('/query2', methods=['GET', 'POST'])
def query2():
    if request.method == 'POST':
        cu = mysql.connection.cursor()
        #Lista de comenzi cu detalii despre client și angajatul care a gestionat comanda
        cu.execute("SELECT Comenzi.Id_comanda,Comenzi.Data_comenzii,Clienti.Nume AS Client_Nume,Clienti.Prenume AS Client_Prenume,Clienti.Email AS Client_Email,Angajati.Nume AS Angajat_Nume,Angajati.Prenume AS Angajat_Prenume FROM Comenzi JOIN Clienti ON Comenzi.Clienti = Clienti.Id_client JOIN Angajati ON Comenzi.Angajat = Angajati.Id_angajat")
        results1 = cu.fetchall()
        #Lista pentru toate detaliile comenzii, inclusiv informații despre produs pentru o anumită comandă
        cu.execute("SELECT Comenzi.Id_comanda,Produse.Nume AS Produs_Nume,Detalii_comanda.Cantitate,Produse.Pret,(Detalii_comanda.Cantitate * Produse.Pret) AS Total FROM Detalii_comanda JOIN Produse ON Detalii_comanda.Produs = Produse.Id_produs JOIN Comenzi ON Detalii_comanda.Comanda = Comenzi.Id_comanda WHERE Comenzi.Id_comanda = 1")
        results2 = cu.fetchall()
        cu.close()
        return render_template('interfata_interogare_2.html', results1=results1, results2=results2)
    

# minim 1 sub-interogare
@app.route('/query3', methods=['GET', 'POST'])
def query3():
    if request.method == 'POST':
        cu = mysql.connection.cursor()
        #Lista pentru toate comenzile împreună cu suma totală pentru fiecare comandă
        cu.execute("SELECT Comenzi.Id_comanda,Comenzi.Data_comenzii,(SELECT SUM(Detalii_comanda.Cantitate * Produse.Pret) FROM Detalii_comanda JOIN Produse ON Detalii_comanda.Produs = Produse.Id_produs WHERE Detalii_comanda.Comanda = Comenzi.Id_comanda) AS Valoare_Totala FROM Comenzi;")
        result = cu.fetchall()
        cu.close()
        return render_template('interfata_interogare_3.html', result=result)

# minim 1 funcție scalară și 1 funcție agregat
@app.route('/query4', methods=['GET', 'POST'])
def query4():
    if request.method == 'POST':
        cu = mysql.connection.cursor()
        #Lista pentru salariul mediu al angajaților, precum și cel mai mare salariu al angajaților
        #functie scalara
        cu.execute("SELECT Id_angajat,CONCAT(Nume, ' ', Prenume) AS Nume_Complet,CONCAT('$', FORMAT(Salariu, 2)) AS Salariu_Formatat FROM Angajati")
        results1 = cu.fetchall()
        #Lista pentru numele fiecărui produs și suma totală a vânzărilor
        #functie agregat
        cu.execute("SELECT Produse.Nume AS Nume_Produs,SUM(Detalii_comanda.Cantitate * Produse.Pret) AS Total_Vanzari FROM Detalii_comanda JOIN Produse ON Detalii_comanda.Produs = Produse.Id_produs GROUP BY Produse.Nume")
        results2 = cu.fetchall()
        cu.close()
        return render_template('interfata_interogare_4.html', results1=results1,results2=results2)



# trigger
#def trigger():


if __name__ == '__main__':
    app.run(debug=True)