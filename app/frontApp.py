from flask import Flask, render_template, request, redirect, url_for, session, flash
from idsServer import payload_types
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

app.config['SECRET_KEY'] = 'amanbangetgess'
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://root:@localhost/yuk_mari'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy object
db = SQLAlchemy(app)

# Model Log
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

# Route halaman EXPORT
@app.route('/export')
def export():
    return render_template('export.html')

# Route halaman LOGINUSER
@app.route('/loginuser')
def loginuser():
    return render_template('loginuser.html')

# Route halaman ACCOUNT_SETTINGS
@app.route('/account_settings')
def account_settings():
    return render_template('account_settings.html')

# Route halaman Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        flash('Silahkan login dulu', 'warning')
        return redirect(url_for('login'))

    return render_template('dashboard.html')

# Model User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) # id auto-increment
    email = db.Column(db.String(150), unique=True, nullable=False) # email harus unik
    password_hash = db.Column(db.String(256), nullable=False) # password hash

    # Menyimpan password dalam bentuk hash
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Memeriksa apakah password cocok dengan hash di database
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    
    def __repr__(self):
        return f"<User {self.email}>"
    
with app.app_context():
        db.create_all()
        print("Database dan tabel berhasil dibuat!")

        # Tambahkan user baru jika belum ada
        if not User.query.filter_by(email="admin@example.com").first():
            new_user = User(email="admin@example.com")
            new_user.set_password("password123")  # Hash password sebelum menyimpan
            db.session.add(new_user)
            db.session.commit()
            print("User berhasil ditambahkan!")
            
# Route halaman LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # cek apakah email user telah terdaftar di database
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session['user'] = user.email
            print(f"User {session['user']} berhasil login")  # Debugging
            flash('Berhasil login', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Email atau Password salah, try again', 'error')
        
    return render_template('login.html')

# Routing halaman Index - Test Input POST Method
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
        email = request.form.get('email')

        if not email:
            flash("Email harus diisi!", "danger")
            return redirect(url_for('reset_password'))

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