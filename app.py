from flask import (
    Flask,
    jsonify,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import secrets
import string
from mail import send_mail
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user.db"
db = SQLAlchemy(app)
app.config["SECRET_KEY"] = "fox"

mail_password = os.environ.get("MAIL_PASSWORD")


# Modèle User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    postal_code = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(15), nullable=False)
    status = db.Column(db.String(50), nullable=True)
    occupation = db.Column(db.String(50), nullable=True)
    education = db.Column(db.String(50), nullable=True)
    salary = db.Column(db.String(50), nullable=True)
    expecting_child = db.Column(db.String(10), nullable=True)
    media = db.Column(db.String(100), nullable=True)
    phone_brand = db.Column(db.String(100), nullable=True)
    reads_magazines = db.Column(db.String(10), nullable=True)
    smokes = db.Column(db.String(10), nullable=True)
    cigarette_brand = db.Column(db.String(100), nullable=True)
    smoking_frequency = db.Column(db.String(50), nullable=True)
    sports = db.Column(db.String(100), nullable=True)


# Modèle Userlogin
class Userlogin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    mail = db.Column(db.String(200), nullable=False)
    activate = db.Column(db.Boolean, default=False)
    activation_token = db.Column(db.String(100), unique=True)

    def __repr__(self):
        return f"<Userlogin {self.username}>"


# Fonction pour générer un token d'activation
def generate_activation_token():
    token = "".join(
        secrets.choice(string.ascii_letters + string.digits) for _ in range(20)
    )
    return token


# Fonction pour initialiser la base de données
def initialize_database():
    with app.app_context():
        db.create_all()

        # Vérifie si superadmin existe dans les deux tables
        superadmin_user = User.query.filter_by(email="superadmin@example.com").first()
        superadmin_login = Userlogin.query.filter_by(username="superadmin").first()

        if not superadmin_user and not superadmin_login:
            # Crée superadmin dans la table User
            superadmin_user = User(
                id=1,
                first_name="Super",
                last_name="Admin",
                gender="homme",
                birth_date=datetime(1970, 1, 1),
                address="123 Admin Street",
                postal_code="00000",
                city="Admin City",
                email="superadmin@example.com",
                phone="0000000000",
                status="admin",
                occupation="Administrator",
                education="N/A",
                salary="N/A",
                expecting_child="N/A",
                media="N/A",
                phone_brand="N/A",
                reads_magazines="N/A",
                smokes="N/A",
                cigarette_brand="N/A",
                smoking_frequency="N/A",
                sports="N/A",
            )
            db.session.add(superadmin_user)

            # Crée superadmin dans la table Userlogin avec le même ID
            superadmin_login = Userlogin(
                id=superadmin_user.id,
                username="superadmin",
                password=generate_password_hash("superadmin"),
                mail=superadmin_user.email,
                activate=True,
                activation_token=None,
            )
            db.session.add(superadmin_login)
            db.session.commit()


# Route pour la page d'accueil
@app.route("/")
def home():
    return render_template("index.html")


# Route pour l'enregistrement d'un nouvel utilisateur
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        mail = request.form["email"]

        activation_token = generate_activation_token()

        new_user = Userlogin(
            username=username,
            password=generate_password_hash(password),
            activation_token=activation_token,
            mail=mail,
        )
        db.session.add(new_user)
        db.session.commit()

        activation_link = url_for(
            "activate_account", token=activation_token, _external=True
        )
        body = f"Merci de vous inscrire. Cliquez sur ce lien pour activer votre compte : {activation_link}"

        from_address = "clement.perchais@live.fr"
        to_address = mail
        subject = "Activation de votre compte"

        if send_mail(from_address, to_address, subject, body, mail_password):
            flash(
                "Un e-mail de validation a été envoyé à votre adresse. Veuillez vérifier pour activer votre compte."
            )
            return redirect(url_for("home"))
        else:
            flash(
                "Erreur lors de l'envoi de l'e-mail de validation. Veuillez réessayer."
            )
            return redirect(url_for("register"))

    return render_template("register.html")


# Route pour l'activation du compte utilisateur
@app.route("/activate/<token>")
def activate_account(token):
    user = Userlogin.query.filter_by(activation_token=token).first()
    if user:
        user.activate = True
        db.session.commit()
        flash(
            "Votre compte a été activé avec succès. Vous pouvez maintenant vous connecter."
        )
    else:
        flash("Le lien d'activation est invalide ou a expiré.")
    return redirect(url_for("home"))


# Route pour la connexion utilisateur
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = Userlogin.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            if user.activate:
                session["username"] = username
                flash("Login successful!")
                return redirect(url_for("home"))
            else:
                flash("Account is deactivated. Please contact support.")
        else:
            flash("Invalid username or password.")
    return render_template("login.html")


@app.route("/add-user", methods=["GET", "POST"])
def add_user():
    if request.method == "POST":
        email = request.form["email"]
        existing_user = User.query.filter_by(email=email).first()
        existing_login = Userlogin.query.filter_by(mail=email).first()

        if existing_user or existing_login:
            flash(
                "Un utilisateur avec cet email existe déjà. Veuillez utiliser un email différent."
            )
            return redirect(url_for("add_user"))

        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        gender = request.form["gender"]
        birth_date = datetime.strptime(request.form["birth_date"], "%Y-%m-%d")
        address = request.form["address"]
        postal_code = request.form["postal_code"]
        city = request.form["city"]
        phone = request.form["phone"]
        status = request.form.get("status")
        occupation = request.form.get("occupation")
        education = request.form.get("education")
        salary = request.form.get("salary")
        expecting_child = request.form.get("expecting_child")
        media = request.form.get("media")
        phone_brand = request.form.get("phone_brand")
        reads_magazines = request.form.get("reads_magazines")
        smokes = request.form.get("smokes")
        cigarette_brand = request.form.get("cigarette_brand")
        smoking_frequency = request.form.get("smoking_frequency")
        sports = request.form.get("sports")

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            birth_date=birth_date,
            address=address,
            postal_code=postal_code,
            city=city,
            email=email,
            phone=phone,
            status=status,
            occupation=occupation,
            education=education,
            salary=salary,
            expecting_child=expecting_child,
            media=media,
            phone_brand=phone_brand,
            reads_magazines=reads_magazines,
            smokes=smokes,
            cigarette_brand=cigarette_brand,
            smoking_frequency=smoking_frequency,
            sports=sports,
        )

        db.session.add(new_user)
        db.session.commit()

        # Génération et stockage du token de validation
        activation_token = generate_activation_token()

        new_userlogin = Userlogin(
            id=new_user.id,  # Set the ID to match the User ID
            username=request.form["username"],
            password=generate_password_hash(request.form["password"]),
            mail=email,
            activation_token=activation_token,
            activate=False,
        )
        db.session.add(new_userlogin)
        db.session.commit()

        flash("User added successfully!")

        activation_link = url_for(
            "activate_account", token=activation_token, _external=True
        )

        body = f"Merci de vous inscrire. Cliquez sur ce lien pour activer votre compte : {activation_link}"

        from_address = "clement.perchais@live.fr"
        to_address = email
        subject = "Activation de votre compte"

        if send_mail(from_address, to_address, subject, body, mail_password):
            flash(
                "Un e-mail de validation a été envoyé à votre adresse. Veuillez vérifier pour activer votre compte."
            )
            return redirect(url_for("add_user_success"))
        else:
            flash(
                "Erreur lors de l'envoi de l'e-mail de validation. Veuillez réessayer."
            )
            return redirect(url_for("register"))
    return render_template("add-user.html")


# Route pour la page de succès d'ajout d'utilisateur
@app.route("/add-user-success")
def add_user_success():
    return render_template("registration_success.html")


# Route pour la page d'administration
@app.route("/admin", methods=["GET", "POST"])
def admin():
    page = request.args.get("page", 1, type=int)
    users = User.query.paginate(page=page, per_page=5)
    userlogins = Userlogin.query.paginate(page=page, per_page=5)
    return render_template("admin.html", users=users, userlogins=userlogins)


# Route pour la page de recherche pannel
@app.route("/pannel_research", methods=["GET", "POST"])
def pannel_research():
    return render_template("pannel_research.html")


@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form["email"]
        user = Userlogin.query.filter_by(mail=email).first()
        if user:
            reset_token = generate_activation_token()
            user.activation_token = reset_token
            db.session.commit()
            reset_link = url_for("reset_password", token=reset_token, _external=True)
            body = f"Veuillez cliquer sur le lien suivant pour réinitialiser votre mot de passe : {reset_link}"
            from_address = "clement.perchais@live.fr"
            to_address = email
            subject = "Réinitialisation de votre mot de passe"
            if send_mail(from_address, to_address, subject, body, mail_password):
                flash("Un email de réinitialisation a été envoyé.")
            else:
                flash(
                    "Erreur lors de l'envoi de l'email de réinitialisation. Veuillez réessayer."
                )
        else:
            flash("Aucun compte associé à cet email.")
        return redirect(url_for("login"))
    return render_template("forgot_password.html")


@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    user = Userlogin.query.filter_by(activation_token=token).first()
    if user:
        if request.method == "POST":
            new_password = request.form["password"]
            user.password = generate_password_hash(new_password)
            user.activation_token = None
            db.session.commit()
            flash(
                "Votre mot de passe a été réinitialisé avec succès. Vous pouvez maintenant vous connecter."
            )
            return redirect(url_for("login"))
        return render_template("reset_password.html", token=token)
    else:
        flash("Le lien de réinitialisation est invalide ou a expiré.")
        return redirect(url_for("login"))


# Route pour supprimer un utilisateur
@app.route("/delete-user/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("admin"))


# Route pour vérifier si un email existe déjà dans la base de données
@app.route("/check-email", methods=["POST"])
def check_email():
    email = request.json["email"]
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({"exists": True})
    else:
        return jsonify({"exists": False})


# Route pour se déconnecter
@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("You have been logged out.")
    return redirect(url_for("home"))


@app.route("/send-email", methods=["POST"])
def send_email():
    data = request.get_json()
    if "formData" not in data or "emails" not in data:
        return jsonify(
            {"success": False, "error": "Les données du formulaire sont manquantes."}
        )

    questions = data["formData"]["questions"]
    emails = data["emails"]

    # Construction du corps de l'e-mail avec les réponses du formulaire
    body = "Réponses au questionnaire :\n\n"
    for i, question in enumerate(questions):
        body += f'Question {i + 1}: {question["question"]}\n'
        body += "Réponses:\n"
        for j, answer in enumerate(question["answers"]):
            body += f"{j + 1}. {answer}\n"
        body += "\n"

    # Envoi de l'e-mail à chaque destinataire
    from_address = "clement.perchais@live.fr"
    subject = "Sujet de l'email"

    for email in emails:
        if not send_mail(from_address, email.strip(), subject, body, mail_password):
            return jsonify(
                {"success": False, "error": "Erreur lors de l'envoi de l'e-mail"}
            )

    return jsonify({"success": True})


@app.route("/user_info")
def user_info():
    if "username" in session:
        user_login = Userlogin.query.filter_by(username=session["username"]).first()
        user = User.query.get(user_login.id)
        if user:
            return render_template("user_info.html", user=user)
    flash("Vous devez être connecté pour voir cette page.")
    return redirect(url_for("login"))


if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)
