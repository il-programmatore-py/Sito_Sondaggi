from flask import Flask, render_template, request, redirect, make_response
import sqlite3

def get_info():
    connection = sqlite3.connect('database.db')
    sondaggi = connection.execute('SELECT * FROM sondaggi').fetchall()
    connection.close()
    return sondaggi

def get_info_gia_presenti():
    connection = sqlite3.connect('database.db')
    sondaggi = connection.execute('SELECT * FROM giochi_gia_presenti').fetchall()
    connection.close()
    return sondaggi

def get_info_non_pubbliche():
    connection = sqlite3.connect('database.db')
    sondaggi_non_pubblici = connection.execute('SELECT * FROM sondaggi_non_pubblici').fetchall()
    connection.close()
    return sondaggi_non_pubblici

def get_accounts():
    connection = sqlite3.connect('database_accounts.db')
    accounts = connection.execute('SELECT * FROM accounts').fetchall()
    connection.close()
    return accounts

def get_accounts_admin():
    connection = sqlite3.connect('database_accounts_admin.db')
    accounts = connection.execute('SELECT * FROM accounts').fetchall()
    connection.close()
    return accounts

def delete(idx):
    connection = sqlite3.connect('database.db')
    connection.execute('DELETE FROM sondaggi_non_pubblici WHERE id=?', (idx,))
    connection.commit()
    connection.close()

def creare(nome, link_img, genere, trailer,descrizione,age, voto_uno, voto_due):
    global sondaggi_values,clients
    cookie = request.cookies.get('Cookie')
    accounts = get_accounts()
    email= ''
    for cosa  in accounts:
        idx, eml, pws, cookie_temp = cosa
        if cookie==cookie_temp:
            email=eml
            break
    try:
        sondaggi = get_info()
        last_idx = int(sondaggi[-1][0])+1
        sondaggi_values[last_idx] = [clients, []]
    except:
        fsd = 0
    connection = sqlite3.connect('database.db')
    connection.execute('INSERT INTO sondaggi_non_pubblici (opzione_uno, opzione_due, voto_uno, voto_due,persona, Generi, trailer,descrizione, age) VALUES (?,?,?,?,?,?,?,?,?)',(nome,link_img, str(voto_uno),str(voto_due), email, genere, trailer,descrizione,age))
    connection.commit()
    connection.close()

def edit_admin_name(text, link_img,generi,trailer,descrizione,age,idx):
    connection = sqlite3.connect('database.db')
    connection.execute('''UPDATE sondaggi_non_pubblici
    SET opzione_uno = ?
    WHERE id=?''', (str(text),idx))
    connection.execute('''UPDATE sondaggi_non_pubblici
    SET opzione_due = ?
    WHERE id=?''', (str(link_img),idx))
    connection.execute('''UPDATE sondaggi_non_pubblici
    SET Generi = ?
    WHERE id=?''', (str(generi),idx))
    connection.execute('''UPDATE sondaggi_non_pubblici
    SET trailer = ?
    WHERE id=?''', (str(trailer),idx))
    connection.execute('''UPDATE sondaggi_non_pubblici
    SET descrizione = ?
    WHERE id=?''', (str(descrizione),idx))
    connection.execute('''UPDATE sondaggi_non_pubblici
    SET age = ?
    WHERE id=?''', (str(age),idx))
    connection.commit()
    connection.close()

def creare_admin(nome, link_img, genere, trailer,descrizione,age, voto_uno, voto_due):
    global sondaggi_values,clients
    try:
        sondaggi = get_info()
        last_idx = int(sondaggi[-1][0])+1
        sondaggi_values[last_idx] = [clients, []]
    except:
        fsd = 0
    connection = sqlite3.connect('database.db')
    connection.execute('INSERT INTO sondaggi (opzione_uno, opzione_due, voto_uno, voto_due,persona, Generi, trailer,descrizione, age) VALUES (?,?,?,?,?,?,?,?,?)',(nome,link_img, str(voto_uno),str(voto_due), genere, trailer,descrizione,age))
    connection.commit()
    connection.close()

if __name__ == '__main__':
    print('Ciao')


