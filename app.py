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
from datetime import datetime  # Import datetime
import secrets
import string
from mail import send_mail

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user.db"
db = SQLAlchemy(app)
app.config["SECRET_KEY"] = "fox"


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


class Userlogin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    mail = db.Column(db.String(200), nullable=False)

    activate = db.Column(db.Boolean, default=True)
    activation_token = db.Column(db.String(100), unique=True)

    def __repr__(self):
        return f"<Userlogin {self.username}>"


def generate_activation_token():
    token = "".join(
        secrets.choice(string.ascii_letters + string.digits) for _ in range(20)
    )
    return token


# Function to initialize the database with a superadmin user
def initialize_database():
    with app.app_context():
        db.create_all()
        """
        # Check if superadmin exists
        superadmin = Userlogin.query.filter_by(username="superadmin").first()
        if not superadmin:
            # Create superadmin user
            superadmin = Userlogin(
                id=2, username="superadmin", password="superadmin", activate=True
            )
            db.session.add(superadmin)
            db.session.commit()

            """


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        mail = request.form["email"]
        # Génération et stockage du token de validation
        activation_token = generate_activation_token()

        new_user = Userlogin(
            username=username,
            password=password,
            activation_token=activation_token,
            mail=mail,
        )
        db.session.add(new_user)
        db.session.commit()

        # Envoi de l'e-mail de validation
        activation_link = url_for(
            "activate_account", token=activation_token, _external=True
        )
        body = f"Merci de vous inscrire. Cliquez sur ce lien pour activer votre compte : {activation_link}"

        from_address = "clement.perchais@live.fr"
        to_address = "clement.perchais@live.fr"
        subject = "Sujet de l'email"
        password = "arveclgu69"
        print(
            activation_link,
        )
        if send_mail(from_address, to_address, subject, body, password):
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


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = Userlogin.query.filter_by(username=username, password=password).first()
        if user:
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
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        gender = request.form["gender"]
        birth_date = datetime.strptime(request.form["birth_date"], "%Y-%m-%d")
        address = request.form["address"]
        postal_code = request.form["postal_code"]
        city = request.form["city"]
        email = request.form["email"]
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

        # Use the same ID for the Userlogin

        # Génération et stockage du token de validation
        activation_token = generate_activation_token()

        new_userlogin = Userlogin(
            id=new_user.id,  # Set the ID to match the User ID
            username=request.form["username"],
            password=request.form["password"],
            mail=request.form["email"],
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
        to_address = request.form["email"]
        subject = "Sujet de l'email"
        password = ""
        print(
            activation_link,
        )
        if send_mail(from_address, to_address, subject, body, password):
            flash(
                "Un e-mail de validation a été envoyé à votre adresse. Veuillez vérifier pour activer votre compte."
            )
            return redirect(url_for("add_user_success"))
        else:
            flash(
                "Erreur lors de l'envoi de l'e-mail de validation. Veuillez réessayer."
            )
            return redirect(url_for("register"))
    return render_template(("add-user.html"))


@app.route("/add-user-success")
def add_user_success():
    return render_template("registration_success.html")


@app.route("/admin", methods=["GET", "POST"])
def admin():
    page = request.args.get("page", 1, type=int)
    users = User.query.paginate(page=page, per_page=5)
    userlogins = Userlogin.query.paginate(page=page, per_page=5)  # Fetch Userlogin data
    return render_template("admin.html", users=users, userlogins=userlogins)


@app.route("/pannel_research", methods=["GET", "POST"])
def pannel_research():
    return render_template("pannel_research.html")


@app.route("/delete-user/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("admin"))


@app.route("/registration_success")
def registration_success():
    return render_template("registration_success.html")


@app.route("/check-email", methods=["POST"])
def check_email():
    email = request.json["email"]
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({"exists": True})
    else:
        return jsonify({"exists": False})


@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("You have been logged out.")
    return redirect(url_for("home"))


if __name__ == "__main__":
    initialize_database()  # Initialize database with superadmin if not already present
    app.run(debug=True)
