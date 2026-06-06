---
- name: Konfigurasi Full Stack Kas RW 25 dengan Rekap Tabel
  hosts: localhost
  connection: local
  become: yes
  tasks:
    # ==========================================
    # BAGIAN 1: DATABASE (MySQL)
    # ==========================================
    - name: Setup Database
      block:
        - name: Install MySQL Server
          apt:
            name: mysql-server
            state: present
            update_cache: yes

        - name: Konfigurasi Akses Remote MySQL
          lineinfile:
            path: /etc/mysql/mysql.conf.d/mysqld.cnf
            regexp: '^bind-address'
            line: 'bind-address = 0.0.0.0'

        - name: Setup User dan Tabel Kas
          shell: |
            mysql -e "CREATE DATABASE IF NOT EXISTS db_kasrw;"
            mysql -e "CREATE USER IF NOT EXISTS 'admin_kas'@'%' IDENTIFIED BY 'password123';"
            mysql -e "GRANT ALL PRIVILEGES ON db_kasrw.* TO 'admin_kas'@'%';"
            mysql -e "USE db_kasrw; CREATE TABLE IF NOT EXISTS transaksi (
              id INT AUTO_INCREMENT PRIMARY KEY,
              tanggal DATE,
              keterangan VARCHAR(255),
              tipe ENUM('masuk', 'keluar'),
              jumlah DECIMAL(15, 2)
            );"
            mysql -e "FLUSH PRIVILEGES;"

        - name: Restart MySQL
          service:
            name: mysql
            state: restarted
      when: target_node == 'database'

    # ==========================================
    # BAGIAN 2: BACKEND (Python Flask)
    # ==========================================
    - name: Setup Backend API
      block:
        - name: Install Python Libs
          apt:
            name:
              - python3-pip
              - python3-flask
              - python3-flask-cors
              - python3-mysqldb
            state: present

        - name: Deploy Source Code App.py
          copy:
            dest: "/home/vagrant/app.py"
            content: |
              from flask import Flask, request, jsonify
              from flask_cors import CORS
              import MySQLdb
              import MySQLdb.cursors
              app = Flask(__name__)
              CORS(app)

              def get_db():
                return MySQLdb.connect(host="192.168.56.11", user="admin_kas", passwd="password123", db="db_kasrw", cursorclass=MySQLdb.cursors.DictCursor)

              @app.route('/api/transaksi', methods=['POST'])
              def add():
                d = request.json
                db = get_db(); cur = db.cursor()
                cur.execute("INSERT INTO transaksi (tanggal, keterangan, tipe, jumlah) VALUES (%s,%s,%s,%s)", (d['tanggal'], d['keterangan'], d['tipe'], d['jumlah']))
                db.commit(); db.close()
                return jsonify({"status": "sukses"})

              @app.route('/api/transaksi', methods=['GET'])
              def get_all():
                db = get_db(); cur = db.cursor()
                cur.execute("SELECT DATE_FORMAT(tanggal, '%d/%m/%Y') as tanggal, keterangan, tipe, jumlah FROM transaksi ORDER BY id DESC")
                res = cur.fetchall(); db.close()
                return jsonify(res)

              @app.route('/api/laporan', methods=['GET'])
              def rep():
                db = get_db(); cur = db.cursor()
                cur.execute("SELECT SUM(CASE WHEN tipe='masuk' THEN jumlah ELSE 0 END) as m, SUM(CASE WHEN tipe='keluar' THEN jumlah ELSE 0 END) as k FROM transaksi")
                res = cur.fetchone(); db.close()
                m, k = float(res['m'] or 0), float(res['k'] or 0)
                return jsonify({"masuk": m, "keluar": k, "saldo": m - k})

              if __name__ == '__main__':
                app.run(host='0.0.0.0', port=5000)

        - name: Start Backend Service
          shell: "nohup python3 /home/vagrant/app.py > /home/vagrant/app.log 2>&1 &"
      when: target_node == 'backend'

    # ==========================================
    # BAGIAN 3: FRONTEND (Nginx)
    # ==========================================
    - name: Setup Web Dashboard
      block:
        - name: Install Nginx
          apt:
            name: nginx
            state: present

        - name: Deploy Dashboard
          copy:
            dest: "/var/www/html/index.html"
            content: |
              <!DOCTYPE html>
              <html lang="id">
              <head>
                <meta charset="UTF-8">
                <title>Sistem Kas RW 25</title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
                <style>
                  body { background-color: #f0f2f5; font-family: 'Inter', sans-serif; padding: 20px; }
                  .card { border: none; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
                  .header-banner { background: #1a4da1; color: white; padding: 25px; border-radius: 12px 12px 0 0; text-align: center; }
                  .btn-simpan { background-color: #28a745; color: white; font-weight: 600; border: none; }
                  .saldo-text { font-size: 1.5rem; font-weight: 700; color: #1a4da1; }
                  .badge-pemasukan { background-color: #d1e7dd; color: #0f5132; }
                  .badge-pengeluaran { background-color: #f8d7da; color: #842029; }
                </style>
              </head>
              <body>
              <div class="container" style="max-width: 900px;">
                <div class="card mb-4">
                  <div class="header-banner">
                    <h2 class="mb-0">Kas Digital RW 25</h2>
                    <p class="mb-0">Sistem Informasi Pengelolaan Keuangan Warga</p>
                  </div>
                  <div class="card-body p-4">
                    <form id="formKas">
                      <div class="row g-3">
                        <div class="col-md-6">
                          <label class="form-label fw-bold">Tanggal</label>
                          <input type="date" id="tanggal" class="form-control" required>
                        </div>
                        <div class="col-md-6">
                          <label class="form-label fw-bold">Tipe Transaksi</label>
                          <select id="tipe" class="form-select">
                            <option value="masuk">Pemasukan (+)</option>
                            <option value="keluar">Pengeluaran (-)</option>
                          </select>
                        </div>
                        <div class="col-12">
                          <label class="form-label fw-bold">Keterangan</label>
                          <input type="text" id="keterangan" class="form-control" placeholder="Contoh: Iuran Warga April" required>
                        </div>
                        <div class="col-12">
                          <label class="form-label fw-bold">Jumlah (Rp)</label>
                          <input type="number" id="jumlah" class="form-control" placeholder="Contoh: 500000" required>
                        </div>
                        <div class="col-12 mt-4">
                          <button type="submit" class="btn btn-simpan w-100 py-2">Simpan Transaksi</button>
                        </div>
                      </div>
                    </form>
                  </div>
                </div>
                <div class="card p-4">
                  <div class="d-flex justify-content-between align-items-center mb-4">
                    <h4 class="mb-0 text-secondary">Rekapitulasi Transaksi</h4>
                    <div id="displaySaldo" class="saldo-text">Total Saldo: Rp 0</div>
                  </div>
                  <div class="table-responsive">
                    <table class="table table-hover align-middle">
                      <thead class="table-light">
                        <tr><th>Tanggal</th><th>Keterangan</th><th>Tipe</th><th class="text-end">Jumlah</th></tr>
                      </thead>
                      <tbody id="tabelBody"></tbody>
                    </table>
                  </div>
                </div>
              </div>
              <script>
                const API_URL = 'http://192.168.56.10:5000/api/transaksi';
                async function muatData() {
                  try {
                    const response = await fetch(API_URL);
                    const data = await response.json();
                    const tabelBody = document.getElementById('tabelBody');
                    tabelBody.innerHTML = '';
                    let totalSaldo = 0;
                    data.forEach(item => {
                      const nominal = parseFloat(item.jumlah);
                      const isPemasukan = item.tipe === 'masuk';
                      if (isPemasukan) totalSaldo += nominal;
                      else totalSaldo -= nominal;
                      tabelBody.innerHTML += `<tr>
                        <td>${item.tanggal}</td>
                        <td>${item.keterangan}</td>
                        <td><span class="badge ${isPemasukan ? 'badge-pemasukan' : 'badge-pengeluaran'}">${item.tipe.toUpperCase()}</span></td>
                        <td class="text-end fw-bold ${isPemasukan ? 'text-success' : 'text-danger'}">${isPemasukan ? '+' : '-'} Rp ${nominal.toLocaleString('id-ID')}</td>
                      </tr>`;
                    });
                    document.getElementById('displaySaldo').innerText = 'Total Saldo: Rp ' + totalSaldo.toLocaleString('id-ID');
                  } catch(e) { console.error(e); }
                }
                document.getElementById('formKas').addEventListener('submit', async function(e) {
                  e.preventDefault();
                  const data = {
                    tanggal: document.getElementById('tanggal').value,
                    keterangan: document.getElementById('keterangan').value,
                    tipe: document.getElementById('tipe').value,
                    jumlah: document.getElementById('jumlah').value
                  };
                  await fetch(API_URL, { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(data) });
                  alert('Data Tersimpan!');
                  muatData();
                });
                muatData();
              </script>
              </body>
              </html>
      when: target_node == 'frontend'