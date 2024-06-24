from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from alembic import op
import sqlalchemy as sa


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
db = SQLAlchemy(app)
migrate = Migrate(app, db)


def upgrade():
    # Add the gender column to the user table
    with op.batch_alter_table("user") as batch_op:
        batch_op.add_column(sa.Column("activate", sa.Boolean(), nullable=False))
    op.add_column("user", sa.Column("gender", sa.String(length=10), nullable=False))


def downgrade():
    # Remove the gender column from the user table
    op.drop_column("user", "gender")


upgrade()
