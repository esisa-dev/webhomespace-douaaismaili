from flask import(
    Flask,
    request,
    render_template,
    redirect,
    session,
    url_for,

)
import logging
from logging.handlers import RotatingFileHandler
from service import UserService
import hashlib
import os
app=Flask(__name__)
app.logger.setLevel(logging.INFO)
handler=RotatingFileHandler('log.txt')
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s'))

app.logger.addHandler(handler)

def generate_key(login):
    return hashlib.md5(str(login).encode('utf-8')).hexdigest()
app.secret_key='1234'
@app.route('/')
def index():
    return render_template('login.html')
@app.route('/login',methods=['POST'])
def login():
    login=request.form['username']
    pwd=request.form['password']
    if(service_User.verifyUser(login,pwd))==True:
        app.secret_key=generate_key(login)
        liste=service_User.listContent(f'/home/{login}')
        #response=app.make_response(render_template('app.html'))
        session['user_id']=login
        #response.set_cookie('access_time',str(datetime.now()))
        app.logger.info('Bienvenue')
        service_User.oldUrl=f'/home/{login}'
        print('Login old:', service_User.oldUrl )
        return render_template('app.html', liste=liste)
    else:
        app.logger.error('login or password incorrect')
        return render_template('login.html',error_auth='login or password incorrect')
@app.route('/logout')
def logout():
    session.pop('user_id',None)
    app.logger.info('Au revoir')
    service_User.c=False
    return redirect(url_for('index'))
 
    
@app.route('/navigate' ,methods=['GET'])
def navigate():
    path=request.args.get('navig')
    liste=service_User.navigate(path)
    if(type(liste))!=str:
        return render_template('app2.html', liste=liste)
    else:
        filename=path.split('/')[len(path.split('/'))-1]
        return render_template('file.html', liste=liste,filename=filename)

@app.route('/rechercher',methods=['GET'])
def rechercher():
    value=request.args.get('recherche')
    liste=service_User.rechercher(value)
    return render_template('rechercher.html', liste=liste,value=value)

@app.route('/compresser',methods=['GET'])
def compresser():
    service_User.compress_directory(service_User.oldUrl)
    app.logger.info('Compress_directory')
    return render_template('compresser.html')
@app.route('/files')
def filesCount():
    count=service_User.filesCount() +' fichiers'
    return render_template('Count.html', count=count)
@app.route('/dirs')
def dirsCount():
    count=service_User.dirsCount() +' repertoires'
    return render_template('Count.html', count=count)
@app.route('/space')
def space():
    liste=service_User.space()
    return render_template('Count.html', liste=liste)
@app.errorhandler(Exception)
def error(exception):
    return render_template('error.html',error=
     {
        "ip":request.remote_addr,
        "method":request.method,
        "error" :Exception.__str__()
    })
if __name__=='__main__':
    service_User=UserService('',False)
    app.run(host="0.0.0.0",debug=True)