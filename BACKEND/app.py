from flask import Flask, request, jsonify
from flask_cors import CORS
import MySQLdb
import MySQLdb.cursors

app = Flask(__name__)
CORS(app)

def get_db():
    return MySQLdb.connect(
        host="192.168.56.11",
        user="studio_user",
        passwd="studio123",
        db="db_studio",
        cursorclass=MySQLdb.cursors.DictCursor
    )

@app.route('/api/booking', methods=['GET'])
def get_all():
    db = get_db(); cur = db.cursor()
    cur.execute("""SELECT id, nama_studio,
        DATE_FORMAT(tanggal, '%d/%m/%Y') as tanggal,
        TIME_FORMAT(jam_mulai, '%H:%i') as jam_mulai,
        TIME_FORMAT(jam_selesai, '%H:%i') as jam_selesai,
        nama_pemesan, no_hp, metode_bayar,
        CAST(harga AS CHAR) as harga, status
        FROM booking ORDER BY id DESC""")
    res = cur.fetchall(); db.close()
    return jsonify(res)

@app.route('/api/booking', methods=['POST'])
def add():
    d = request.json
    db = get_db(); cur = db.cursor()
    cur.execute("""INSERT INTO booking
        (nama_studio, tanggal, jam_mulai, jam_selesai, nama_pemesan, no_hp, metode_bayar, harga)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
        (d['nama_studio'], d['tanggal'], d['jam_mulai'], d['jam_selesai'],
         d['nama_pemesan'], d['no_hp'], d['metode_bayar'], d['harga']))
    db.commit(); db.close()
    return jsonify({"status": "sukses"})

@app.route('/api/booking/<int:id>', methods=['DELETE'])
def delete(id):
    db = get_db(); cur = db.cursor()
    cur.execute("DELETE FROM booking WHERE id=%s", (id,))
    db.commit(); db.close()
    return jsonify({"status": "terhapus"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)