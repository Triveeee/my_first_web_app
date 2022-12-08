from flask import Flask, render_template, request
import pymongo as mongo
import json

password = 'trive004'
atlas = mongo.MongoClient('mongodb+srv://riccardo:trive004@cluster0.zzvi9yy.mongodb.net/test')
db = atlas.cluster0
collection = db.roba


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('inserimento.html')
    
@app.route('/inserimento' , methods=['POST'])
def insert():
    
    titolo = request.form['title']
    film = collection.find_one({'titolo': titolo})

    if(film == None):
        i = 0
        film = collection.find_one({'_id': i})
        while(not (film == None)):
            i+=1
            film = collection.find_one({'_id': i})

        film = {
            "_id": i,
            "titolo": titolo , 
            "genere": request.form['genere'],
        }

        collection.insert_one(film)
        return 'inserimento avvenuto con sucesso'
    else :
        return 'film gia esistente'

@app.route('/lettura')
def lettura():
    elencofilm = collection.find()
    elencofilm = list(elencofilm)
    elencofilm = json.dumps(elencofilm)
    return elencofilm
