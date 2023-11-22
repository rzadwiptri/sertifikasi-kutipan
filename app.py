import os
from pymongo import MongoClient
import jwt
from datetime import datetime, timedelta
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from bson import ObjectId 

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "./static/profile_pics"
app.config["SECRET_KEY"] = "SPARTA"
app.config["TOKEN_KEY"] = "mytoken"

cxn_str = 'mongodb+srv://rzadwiptri:kelompok5@cluster0.sbzask3.mongodb.net/'
client = MongoClient(cxn_str)

db = client.db_sertifikasi

@app.route('/')
def index():
    kutipan = db.kutipan.find()
    return render_template('index.html', kutipan=kutipan)

@app.route('/add_quote', methods=['POST'])
def add_quote():
    if request.method == 'POST':
        kutipan = request.form['kutipan']
        now = datetime.now() 
        date_time = now.strftime("%Y-%m-%d %H:%M:%S")
        db.kutipan.insert_one({'quote': kutipan, 'created_at': date_time })
        return redirect(url_for('index'))
    

@app.route('/delete_quote/<quote_id>', methods=['GET'])
def delete_quote(quote_id):
    db.kutipan.delete_one({'_id': ObjectId(quote_id)}) 
    return redirect(url_for('index'))

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return f'File {filename} berhasil diunggah'
    
    return 'Tidak ada file yang diunggah atau terjadi kesalahan.'  

@app.route('/detail', methods=['POST'])
def detail():
    if request.method == 'POST':
        kutipan = request.form['kutipan']
        return render_template('detail.html', kutipan=kutipan)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)


