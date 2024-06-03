from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime  # Import datetime


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user.db"
db = SQLAlchemy(app)
migrate = Migrate(app, db)


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


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/add-user", methods=["GET", "POST"])
def add_user():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        gender = request.form["gender"]
        birth_date_str = request.form["birth_date"]
        birth_date = datetime.strptime(
            birth_date_str, "%Y-%m-%d"
        ).date()  # Convert to date object
        address = request.form["address"]
        postal_code = request.form["postal_code"]
        city = request.form["city"]
        email = request.form["email"]
        phone = request.form["phone"]
        status = request.form["status"]
        occupation = request.form["occupation"]
        education = request.form["education"]
        salary = request.form["salary"]
        expecting_child = request.form["expecting_child"]
        media = request.form["media"]
        phone_brand = request.form["phone_brand"]
        reads_magazines = request.form["reads_magazines"]
        smokes = request.form["smokes"]
        cigarette_brand = request.form["cigarette_brand"]
        smoking_frequency = request.form["smoking_frequency"]
        sports = request.form["sports"]

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
        return redirect(url_for("add_user", success=True))
    return render_template("add-user.html")


@app.route("/admin", methods=["GET", "POST"])
def admin():
    page = request.args.get("page", 1, type=int)
    users = User.query.paginate(page=page, per_page=5)
    return render_template("admin.html", users=users)


@app.route("/delete-user/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("admin"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Traitement de l'inscription de l'utilisateur
        # Envoi de l'e-mail de confirmation
        # send_confirmation_email(request.form["email"])
        return redirect(url_for("registration_success"))
    return render_template("register.html")


@app.route("/registration_success")
def registration_success():
    return (
        "Inscription réussie. Un e-mail de confirmation a été envoyé à votre adresse."
    )


app.route("/check-email", methods=["POST"])

def check_email():

    email = request.json["email"]
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({"exists": True})
    else:
        return jsonify({"exists": False})


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
