from idsServer import payload_types
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

app.config['SECRET_KEY'] = 'amanbangetgess'
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://root:@localhost/yuk_mari'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy object
db = SQLAlchemy(app)

# Define the Log model
class Log(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key=True)
    log_message = db.Column(db.Text, nullable=False)
    log_time = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    ip_src = db.Column(db.String(45))
    tcp_sport = db.Column(db.Integer)
    ip_dst = db.Column(db.String(45))
    tcp_dport = db.Column(db.Integer)
    severity = db.Column(db.String(10))

# fungsi ambil paket serangan
def fetch_attack_data():
    return Log.query.all()

# load paket serangan dan routing ke index
@app.route('/')
def index():
    data = fetch_attack_data()

    return render_template('index.html', data=data)

@app.route('/export')
def export():
    return render_template('export.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email == 'admin@test.com' and password == 'Test123#':
            session['user'] = email
            flash('Berhasil login gesss', 'success')

            return redirect(url_for('index'))
        
        else:
            flash('Salah email atau password gess', 'error')
    
    return render_template('login.html')

# routing test serangan via input dengan method POST
@app.route('/test_input', methods=['POST'])
def test_input():
    test_input = request.form['testInput']
    print(f"Received test input: {test_input}")

    # default severity
    severity = 'INFORMATIVE'

    # jika ada serangan terdeteksi sesuaikan dengan payload
    for attack_name, attack_payloads, attack_severity in payload_types:
        if any(payload in test_input for payload in attack_payloads):
            severity = attack_severity
            break
    
    # simpan ke db
    new_log = Log(
        log_message=test_input,
        ip_src='127.0.0.1',
        tcp_sport=80,
        ip_dst='127.0.0.1',
        tcp_dport=80,
        severity=severity
    )

    db.session.add(new_log)
    db.session.commit()

    return redirect(url_for('index'))

# routing untuk hapus log
@app.route('/delete_log/<int:log_id>', methods=['POST'])
def delete_log(log_id):
    log_to_delete = Log.query.get(log_id)
    if log_to_delete:
        db.session.delete(log_to_delete)
        db.session.commit()

    return redirect(url_for('index'))

    # Route untuk reset password
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    background_image_url = url_for('static', filename='img/background.jpg')  # URL gambar (dipindahkan ke sini)
    if request.method == 'POST':
        email = request.form['email']
        try:
            # Proses reset password (misalnya, kirim email)
            print(f"Email reset password diminta untuk: {email}")
            flash("Permintaan reset password telah diproses. Silakan cek email Anda.", "info")  # Pesan sukses
            return redirect(url_for('login'))  # Redirect ke halaman yang sesuai
        except Exception as e:
            print(f"Terjadi kesalahan: {e}")
            flash("Terjadi kesalahan saat memproses permintaan Anda. Silakan coba lagi nanti.", "danger")  # Pesan kesalahan
            return render_template('resetpass.html')  # Render template lagi agar form tidak hilang
    return render_template('resetpass.html')  # Render template untuk GET request


if __name__ == "__main__":
    app.run(debug=True)