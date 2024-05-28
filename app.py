from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import win32com.client


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    status = db.Column(db.String(50), nullable=True)  # Add the new column


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add-user', methods=['GET', 'POST'])
def add_user():
    
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        address = request.form['address']
        city = request.form['city']
        phone = request.form['phone']
        status = request.form['status']
         
        new_user = User(first_name=first_name, last_name=last_name, email=email, address=address, city=city, phone=phone,status= status)
        db.session.add(new_user)
        db.session.commit()
        send_confirmation_email(request.form['email'])
        return redirect(url_for('add_user', success=True))
    return render_template('add-user.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    page = request.args.get('page', 1, type=int)
    users = User.query.paginate(page=page, per_page=5)
    return render_template('admin.html', users=users)

@app.route('/delete-user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Traitement de l'inscription de l'utilisateur
        # Envoi de l'e-mail de confirmation
        send_confirmation_email(request.form['email'])
        return redirect(url_for('registration_success'))
    return render_template('register.html')

def send_confirmation_email(email):
    ol = win32com.client.Dispatch('Outlook.Application')
    olmailitem = 0x0
    newmail = ol.CreateItem(olmailitem)
    newmail.Subject = 'Confirmation d\'inscription'
    newmail.To = recipients=[email]
    newmail.Body= 'Merci de vous être inscrit sur notre site. Veuillez cliquer sur le lien suivant pour confirmer votre inscription : http://votre-site.com/confirm_registration'
    newmail.Send()

@app.route('/registration_success')
def registration_success():
    return 'Inscription réussie. Un e-mail de confirmation a été envoyé à votre adresse.'

app.route('/check-email', methods=['POST'])
def check_email():
    
    email = request.json['email']
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({'exists': True})
    else:
        return jsonify({'exists': False})



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
