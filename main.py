from flask import Flask, render_template, request, redirect, make_response
from account_Gestor import get_info, get_info_gia_presenti, get_info_non_pubbliche, get_accounts, get_accounts_admin, delete, creare, edit_admin_name, creare_admin
from random import randint
import random
import smtplib
import sqlite3

app = Flask(__name__)

html = ''
clients = []
admin_cookie = []
admin_on = []
links = {}
links_reg= {}
bozza = {}
registrando = {}
sondaggi_values = {}

def modifica_voto_uno(num,idx):
    connection = sqlite3.connect('database.db')
    connection.execute('''UPDATE sondaggi
    SET voto_uno = ?
    WHERE id=?''', (num,idx))
    connection.commit()
    connection.close()
def modifica_pw(pws,idx):
    connection = sqlite3.connect('/home/5DSondaggi/mysite/database_accounts.db')
    connection.execute('''UPDATE accounts
    SET pws = ?
    WHERE email=?''', (pws,idx))
    connection.commit()
    connection.close()
@app.route('/')
def Home():
    global html, clients
    html = '''<title>5D Sondaggi</title>
    <nav class="navbar navbar-dark bg-dark">
  <a class="navbar-brand" href="/">
    <img src="img.jpg" width="30" height="30" class="d-inline-block align-top" alt="">
    Sito Per Sondaggi
  </a>
  <div class="form-inline">
        <div class="container mx-5">
            <div class="row">
                <div class="col-sm">
                    <a href="/login" class="btn btn-success my-2 my-sm-0">Login</a>
                    <a href="/sign_up" class="btn btn-success my-2 my-sm-0">Sign Up</a>
                </div>
            </div>
        </div>
  </div>
</nav>
<div class="container my-5">
      <h1 class="display-4">Sito Per Sondaggi</h1><h1>
        <p class="lead">Descrizione Del SIto</p>
        <a class="btn btn-primary" href="/" role="button">Home</a>
        <a class="btn btn-primary" href="/giochi_presenti" role="button">Giochi Presenti</a>
        
        <a class="btn btn-secondary" href="/Crea" role="button">Crea</a>
        <a class="btn btn-danger" href="/admin" role="button">Admin</a>
    </h1></div>'''
    resp = request.cookies.get('Cookie')
    html+='<div class="container my-sm"><div class="row">'
    sondaggi = get_info()
    for cosa in sondaggi:
        idx_temp, opzione_uno, opzione_due, voto_uno, voto_due, generi, trailer,descrizione, age, piattaforma = cosa # per ogni sondaggio in sondaggi
        vote =''
        votish = []
        for voto in voto_due:
            if voto!='-':
                vote+=voto
            else:
                votish.append(vote)
                vote = ''
        if resp not in votish:
            if voto_uno < 15:
                html+=f'<div class="col-sm"><div class="card" style="width: 20rem;"><img class="card-img-top" src="{opzione_due}" alt="Card image cap"><div class="card-body"><h5 class="card-title">{opzione_uno}</h5><p class="h5 card-text">Voti: {voto_uno} su 15</p><div class="col-sm"><a type="button" class="btn btn-secondary btn-lg btn-block" href="/{idx_temp}/info_gioco">Info Gioco</a><a href="{idx_temp}/voto/1"  type="button" class="btn btn-primary btn-lg btn-block">Vota {opzione_uno}</a></div></div></div></div>'
            else:
                html+=f'<div class="col-sm"><div class="card" style="width: 20rem;"><img class="card-img-top" src="{opzione_due}" alt="Card image cap"><div class="card-body"><h5 class="card-title">{opzione_uno}</h5><p class="h5 card-text">Voti: 15 su 15</p><div class="col-sm"><a type="button" class="btn btn-secondary btn-lg btn-block" href="/{idx_temp}/info_gioco">Info Gioco</a><a type="button" class="btn btn-danger btn-lg btn-block">Voti raggiunti</a></div></div></div></div>'
        else:
            if voto_uno < 15:
                html+=f'<div class="col-sm"><div class="card" style="width: 20rem;"><img class="card-img-top" src="{opzione_due}" alt="Card image cap"><div class="card-body"><h5 class="card-title">{opzione_uno}</h5><p class="h5 card-text">Voti: {voto_uno} su 15</p><div class="col-sm"><a type="button" class="btn btn-secondary btn-lg btn-block" href="/{idx_temp}/info_gioco">Info Gioco</a><a type="button" class="btn btn-success btn-lg btn-block">Hai Gia Votato</a></div></div></div></div>'
            else:
                html+=f'<div class="col-sm"><div class="card" style="width: 20rem;"><img class="card-img-top" src="{opzione_due}" alt="Card image cap"><div class="card-body"><h5 class="card-title">{opzione_uno}</h5><p class="h5 card-text">Voti: 15 su 15</p><div class="col-sm"><a type="button" class="btn btn-secondary btn-lg btn-block" href="/{idx_temp}/info_gioco">Info Gioco</a><a type="button" class="btn btn-danger btn-lg btn-block">Voti raggiunti</a></div></div></div></div>'
    html+='</div><div class="alert alert-danger" role="alert">Ti Ricordo Di Eseguire il login per votare e creare</div></div><link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.1.3/dist/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">'

    return html

def send_Email(emailn,contenuto):
    email = smtplib.SMTP("smtp.gmail.com", 587)
    email.ehlo()
    email.starttls()
    email.login('Tua_Email',"password")
    email.sendmail('Tua_Email',str(emailn),contenuto)
    email.quit()

@app.route('/sign_up')
def sign_up():
    global links_reg
    get_email = str(request.args.get('exampleInputEmail1')) # Requests the input- a
    password = str(request.args.get('exampleInputPassword1')) # Requests the input- a
    get_email = get_email.replace(' ','')
    password = password.replace(' ','')
    accounts = get_accounts()
    for cosa in accounts:
        idx, email, pws, cooke = cosa
        if get_email==email:
            html=['danger','Email Gia Usata!!']
            return render_template('sign_up.html',alert=html)
    if get_email!=str(None) and password!=str(None):
        caratteri = '1234567890QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm'
        link = ''
        for x in range(0,20,1):
            link+=random.choice(caratteri)
        links_reg[link]=get_email
        contenuto = f"Subject: Per registrarti su 5dsondaggi.pythonanywhere.com\n\nDevi cliccare il seguente link:/{link}"
        send_Email(get_email,contenuto)
        registrando[link]=password
        html=['success','Email di verifica inviata con successo!!']
        return render_template('sign_up.html',alert=html)
    return render_template('sign_up.html',alert='')


@app.route('/pw_dimenticata')
def pw_dimenticata():
    global links
    email = str(request.args.get('email'))
    if email!=str(None):
        caratteri = '1234567890QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm'
        link = ''
        for x in range(0,20,1):
            link+=random.choice(caratteri)
        links[link]=email
        contenuto=f"Subject: C'e arrivata una richiesta per cambiare la password del suo account di 5dsondaggi.pythonanywhere.com\n\nSe non hai fatto questa richiesta ignora questo messagio altrimenti clicca il seguente link:/{link}"
        send_Email(email,contenuto)
    return render_template('pw_dimenticata.html')

@app.route('/<string:link>')
def test(link):
    global links, links_reg
    if link in links.keys():
        pw = str(request.args.get('exampleInputPassword1'))
        if pw!=str(None):
            modifica_pw(pw,links[link])
        lista=[link,links[link]]
        return render_template('change_password.html',lista=lista)
    if link in links_reg.keys():
        html=['success','Email Confermata']
        cookie_value = str(randint(0,999999999999999999999999999))
        connection = sqlite3.connect('/home/5DSondaggi/mysite/database_accounts.db')
        connection.execute('INSERT INTO accounts (email, pws, cookie) VALUES (?, ?, ?)',(links_reg[link],registrando[link],cookie_value))
        connection.commit()
        connection.close()
        cookie = make_response(render_template('sign_up.html',alert=html),200)
        cookie.set_cookie('Ide',cookie_value)
        return cookie
    return render_template('404.html',link=link)

@app.route('/<int:idx>/voto/<int:num>', methods=('GET',))
def votare(idx, num):
    global html, clients, sondaggi_values
    resp = request.cookies.get('Cookie')
    accounts = get_accounts()
    for cosa in accounts:
        idxs, email, pws, cooke = cosa
        if str(resp)==cooke:
            yes=True
            break
        else:
            yes=False
    sondaggi = get_info()
    if yes==True:
        for cosa in sondaggi:
            idx_temp, opzione_uno, opzione_due, voto_uno, voto_due, generi, trailer,descrizione, age, piattaforma = cosa
            vote =''
            votish = []
            for voto in voto_due:
                if voto!='-':
                    vote+=voto
                else:
                    votish.append(vote)
                    vote = ''
            if resp not in votish:
                if str(idx_temp)==str(idx):
                    modifica_voto_uno(str(voto_uno+1),idx)
                    connection = sqlite3.connect('database.db')
                    connection.execute('''UPDATE sondaggi
                    SET voto_due = ?
                    WHERE id=?''', (f'{voto_due}{resp}-',idx))
                    connection.commit()
                    connection.close()
    else:
        return redirect('/login')
    if num==1:
        return redirect('/')
    elif num==0:
        return redirect(f'/{idx}/info_gioco')
    else:
        return redirect('/')

@app.route('/login')
def login():
    get_email = str(request.args.get('exampleInputEmail1')) # Requests the input- a
    password = str(request.args.get('exampleInputPassword1')) # Requests the input- a
    get_email = get_email.replace(' ','')
    password = password.replace(' ','')
    accounts = get_accounts()
    for cosa in accounts:
        idx, email, pws, cooke = cosa
        if get_email==email and password==pws:
            cookie = make_response(redirect('/Clicca qui per confermare di non essere un bot'),200)
            cookie.set_cookie('Cookie',cooke)
            return cookie
    return render_template('login.html')


@app.route('/admin')
def Admin_login():
    global cookie_value, admin_cookie
    Admin = request.cookies.get('Ide')
    if Admin in admin_cookie:
        return redirect('/admin_zone')
    get_email = str(request.args.get('exampleInputEmail1')) # Requests the input- a
    password = str(request.args.get('exampleInputPassword1')) # Requests the input- a
    get_email = get_email.replace(' ','')
    password = password.replace(' ','')
    accounts = get_accounts_admin()
    for cosa in accounts:
        idx, email, pws = cosa
        if get_email==email and password==pws:
            cookie_value = str(randint(0,999999999999999999999999999))
            admin_cookie.append(cookie_value)
            admin_on.append([get_email,password,cookie_value])
            cookie = make_response(redirect('/Clicca_qui_per_confermare_di_non_essere_un_bot'),200)
            cookie.set_cookie('Ide',cookie_value)
            return cookie
    if get_email!=str(None) and password!=str(None):
        return redirect('/admin')
    return render_template('admin_login.html')


@app.route('/Clicca_qui_per_confermare_di_non_essere_un_bot')
def Clicca_qui_per_confermare_di_non_essere_un_bot_admin():
    return redirect('/admin_zone')

@app.route('/Clicca qui per confermare di non essere un bot')
def Clicca_qui_per_confermare_di_non_essere_un_bot():
    return redirect('/')


@app.route('/Crea', methods=('GET', 'POST',))
def create():
    global bozza
    resp = request.cookies.get('Cookie')
    accounts = get_accounts()
    for cosa in accounts:
        idxs, email, pws, cooke = cosa
        if str(resp)==cooke:
            yes=True
            break
        else:
            yes=False
    if yes==True:
        videogioco = str(request.args.get('videogioco')) # Requests the input- a
        link = str(request.args.get('link')) # Requests the input- a
        Generi = str(request.args.get('Generi'))
        trailer = str(request.args.get('trailer'))
        descrizione = str(request.args.get('descrizione'))
        age = str(request.args.get('age'))
        piattaforma = str(request.args.get('Piattaforma'))
        total = str(request.args.get('total'))
        generi = ['Azione','Sparatutto','Avventura','Stealth','Survival','Horror','RPG']
        generi_1 = ['Gestionale','Simulatore','Tower Defense','Educativo','Rompicapo']
        generi_2 =['Casual','Minigioco','Open World','SandBox','Online','Sportivo']
        send_age = {}
        for genere in generi:
            send_age[genere] = '-outline-'
        for genere_1 in generi_1:
            send_age[genere_1] = '-outline-'
        for genere_2 in generi_2:
            send_age[genere_2] = '-outline-'
        if 'None'!=videogioco.replace(' ','') and 'None'!=link.replace(' ','') and 'None'!=Generi.replace(' ','') and 'None'!=trailer.replace(' ','') and descrizione!='' and ''!= descrizione.replace(' ','')and 'None'!=total and total!='None-1':
            creare(videogioco, link,Generi,trailer,descrizione,age, 0, 0)
            return redirect('/')
        if videogioco!='None':send_age['valore_nome']=videogioco
        if link!='None':send_age['valore_link']=link
        if Generi!='None':send_age['valore_Generi']=Generi
        if trailer!='None':send_age['valore_trailer']=trailer
        if descrizione!='None':send_age['valore_descrizione']=descrizione
        if piattaforma!='None':send_age['valore_Piattaforma']=piattaforma
        if age!=None:
            if age=="3+" or age=="3+-1":
                send_age['age'] = age
                send_age['3+'] = '-'
                send_age['7+'] = '-outline-'
                send_age['12+'] = '-outline-'
                send_age['16+'] = '-outline-'
                send_age['18+'] = '-outline-'
            elif age=="7+" or age=="7+-1":
                send_age['age'] = age
                send_age['3+'] = '-outline-'
                send_age['7+'] = '-'
                send_age['12+'] = '-outline-'
                send_age['16+'] = '-outline-'
                send_age['18+'] = '-outline-'
            elif age=="12+" or age=="12+-1":
                send_age['age'] = age
                send_age['3+'] = '-outline-'
                send_age['7+'] = '-outline-'
                send_age['12+'] = '-'
                send_age['16+'] = '-outline-'
                send_age['18+'] = '-outline-'
            elif age=="16+" or age=="16+-1":
                send_age['age'] = age
                send_age['3+'] = '-outline-'
                send_age['7+'] = '-outline-'
                send_age['12+'] = '-outline-'
                send_age['16+'] = '-'
                send_age['18+'] = '-outline-'
            elif age=="18+" or age=="18+-1":
                send_age['age'] = age
                send_age['3+'] = '-outline-'
                send_age['7+'] = '-outline-'
                send_age['12+'] = '-outline-'
                send_age['16+'] = '-outline-'
                send_age['18+'] = '-'
        if age=='None':
            send_age['3+'] = '-outline-'
            send_age['7+'] = '-outline-'
            send_age['12+'] = '-outline-'
            send_age['16+'] = '-outline-'
            send_age['18+'] = '-outline-'
        return render_template('create.html',send_age=send_age)
    else:
        return redirect('/')


def login_richiesto(function):
    def wrapper(*args, **kwargs):
        global admin_cookie
        Admin = request.cookies.get('Ide')
        html = '''<title>5D Sondaggi</title>
    <nav class="navbar navbar-dark bg-dark">
  <a class="navbar-brand" href="/">
    <img src="img.jpg" width="30" height="30" class="d-inline-block align-top" alt="">
    Sito Per Sondaggi
  </a>
  <div class="form-inline">
        <div class="container mx-5">
            <div class="row">
                <div class="col-sm">
                    <a href="/login" class="btn btn-success my-2 my-sm-0">Login</a>
                    <a href="/sign_up" class="btn btn-success my-2 my-sm-0">Sign Up</a>
                </div>
            </div>
        </div>
  </div>
</nav>
<div class="container my-5">
      <h1 class="display-4">Sito Per Sondaggi</h1><h1>
        <p class="lead">Descrizione Del SIto</p>
        <a class="btn btn-primary" href="/" role="button">Home</a>
        <a class="btn btn-primary" href="/giochi_presenti" role="button">Giochi Presenti</a>
        
        <a class="btn btn-secondary" href="/Crea" role="button">Crea</a>
        <a class="btn btn-danger" href="/admin" role="button">Admin</a>
    </h1></div>

  <div class="container my-sm">
            <h5 class="card-title">Errore 401</h5>
            <p class="lead">Esegui Il Login Da Admin per poter Visualizzare L\'url <strong>/admin_zone</strong></p>
            <a href="/" class="btn btn-primary">Vai alla home</a> <a href="/admin" class="btn btn-danger">Login Da Admin</a>
          </div>
        </div>
      </div>
      <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.1.3/dist/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">'''
        if Admin not in admin_cookie:
            return html # Authorization required
        else:
            return function()

    return wrapper


@app.route('/admin_zone')
@login_richiesto
def Admin_zone():
    html = '''<title>5D Sondaggi</title>
    <nav class="navbar navbar-dark bg-dark">
  <a class="navbar-brand" href="/">
    <img src="img.jpg" width="30" height="30" class="d-inline-block align-top" alt="">
    Sito Per Sondaggi
  </a>
  <div class="form-inline">
        <div class="container mx-5">
            <div class="row">
                <div class="col-sm">
                    <a href="/login" class="btn btn-success my-2 my-sm-0">Login</a>
                    <a href="/sign_up" class="btn btn-success my-2 my-sm-0">Sign Up</a>
                </div>
            </div>
        </div>
  </div>
</nav>
<div class="container my-5">
      <h1 class="display-4">Sito Per Sondaggi</h1><h1>
        <p class="lead">Descrizione Del SIto</p>
        <a class="btn btn-primary" href="/" role="button">Home</a>
        <a class="btn btn-primary" href="/giochi_presenti" role="button">Giochi Presenti</a>
        
        <a class="btn btn-secondary" href="/Crea" role="button">Crea</a>
        <a class="btn btn-danger" href="/admin" role="button">Admin</a>
    </h1></div>'''
    sondaggi_non_pubblici = get_info_non_pubbliche()
    html+='<div class="container my-sm"><div class="row">'
    for cosa in sondaggi_non_pubblici:
        idx, opzione_uno, opzione_due, voto_uno, voto_due, email, generi, trailer,descrizione, age, piattaforma= cosa
        html+=f'<div class="col-sm"><div class="card" style="width: 20rem;"><img class="card-img-top" src="{opzione_due}" alt="Card image cap"><div class="card-body"><h5 class="card-title">{opzione_uno}</h5><div class="col-sm"><a href="/{idx}/delete"  type="button" class="btn btn-danger btn-lg btn-block">Elimina {opzione_uno}</a><a href="/{idx}/edit_admin"  type="button" class="btn btn-primary btn-lg btn-block">Modifica {opzione_uno}</a><a href="/Crea_admin?idx={idx}&videogioco={opzione_uno}&link={opzione_due}"  type="button" class="btn btn-primary btn-lg btn-block">Approva {opzione_uno}</a><small>creato da {email}</small></div></div></div></div>'
    html+='</div></div><link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.1.3/dist/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">'
    return html


@app.route('/giochi_presenti')
def giochi_presenti():
    global html, clients
    html = '''<title>5D Sondaggi</title>
    <nav class="navbar navbar-dark bg-dark">
  <a class="navbar-brand" href="/">
    <img src="https://media.giphy.com/media/LsDEzSopB7RLvuH0lI/giphy.gif" width="30" height="30" class="d-inline-block align-top" alt="">
    5D Votazioni
  </a>
  <div class="form-inline">
        <div class="container mx-5">
            <div class="row">
                <div class="col-sm">
                    <a href="/login" class="btn btn-success my-2 my-sm-0">Login</a>
                    <a href="/sign_up" class="btn btn-success my-2 my-sm-0">Sign Up</a>
                </div>
            </div>
        </div>
  </div>
</nav>
<div class="container my-5">
      <h1 class="display-4">5D Votazioni</h1><h1>
        <p class="lead">Un sito dove puoi votare e proporre videogiochi da aggiungere alla 5D</p>
        <a class="btn btn-primary" href="/" role="button">Home</a>
        <a class="btn btn-primary" href="/giochi_presenti" role="button">Giochi Presenti</a>
        <a class="btn btn-secondary" href="/Crea" role="button">Crea</a>
        <a class="btn btn-danger" href="/admin" role="button">Admin</a>
    </h1></div>'''
    sondaggi = get_info_gia_presenti()
    html+='<div class="container my-sm"><div class="row">'
    for cosa in sondaggi:
        idx, opzione_uno, opzione_due, voto_uno, voto_due, generi, trailer,descrizione, age, piattaforma = cosa
        if voto_uno < 15:
            html+=f'<div class="col-sm"><div class="card" style="width: 20rem;"><img class="card-img-top" src="{opzione_due}" alt="Card image cap"><div class="card-body"><h5 class="card-title">{opzione_uno}</h5><p class="h5 card-text">   </p><div class="col-sm"><a type="button" class="btn btn-secondary btn-lg btn-block" href="/{idx}/info_game">Info Gioco</a><a type="button" class="btn btn-success btn-lg btn-block">Gioco Gia Presente</a></div></div></div></div>'
        else:
            html+=f'<div class="col-sm"><div class="card" style="width: 20rem;"><img class="card-img-top" src="{opzione_due}" alt="Card image cap"><div class="card-body"><h5 class="card-title">{opzione_uno}</h5><p class="h5 card-text">Voti: 15 su 15</p><div class="col-sm"><a type="button" class="btn btn-secondary btn-lg btn-block" href="/{idx}/info_game">Info Gioco</a><a type="button" class="btn btn-danger btn-lg btn-block">Voti raggiunti</a></div></div></div></div>'
    html+='</div></div><link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.1.3/dist/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">'

    return html


@app.route('/<int:idx>/info_game', methods=('GET',))
def info_game(idx):
    info = {}
    sondaggi = get_info_gia_presenti()
    for cosa in sondaggi:
        idx_temp, opzione_uno, opzione_due, voto_uno, voto_due, generi, trailer,descrizione, age, piattaforma = cosa
        if str(idx_temp)==str(idx):
            info['name'] = opzione_uno
            info['img'] = opzione_due
            info['descrizione'] = descrizione
            info['generi'] = generi
            info['age'] = age
            if age=='3+' or age=='7+':
                info['age_color'] = 'success'
            if age=='12+' or age=='16+':
                info['age_color'] = 'warning'
            if age=='18+':
                info['age_color'] = 'danger'
    return render_template('info_game.html', info=info)

@app.route('/<int:idx>/info_gioco', methods=('GET',))
def info_gioco(idx):
    info = {}
    sondaggi = get_info()
    for cosa in sondaggi:
        idx_temp, opzione_uno, opzione_due, voto_uno, voto_due, generi, trailer,descrizione, age, piattaforma = cosa
        if str(idx_temp)==str(idx):
            info['name'] = opzione_uno
            info['img'] = opzione_due
            info['descrizione'] = descrizione
            info['generi'] = generi
            info['trailer'] = trailer
            info['age'] = age
            if age=='3+' or age=='7+':
                info['age_color'] = 'success'
            if age=='12+' or age=='16+':
                info['age_color'] = 'warning'
            if age=='18+':
                info['age_color'] = 'danger'
            resp = request.cookies.get('Cookie')
            vote =''
            votish = []
            for voto in voto_due:
                if voto!='-':
                    vote+=voto
                else:
                    votish.append(vote)
                    vote = ''
            if resp not in votish:
                if voto_uno<15:
                    info['votare'] = f'Vota {opzione_uno}'
                    info['color_button'] = 'primary'
                    info['link_voto'] = f'/{idx_temp}/voto/0'
                else:
                    info['votare'] = 'Voti Raggiunti'
                    info['color_button'] = 'danger'
            else:
                info['votare'] = 'Hai Gia Votato'
                info['color_button'] = 'success'
    return render_template('info_gioco.html', info=info)


app.run(debug=True)







