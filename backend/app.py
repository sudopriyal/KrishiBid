from flask import Flask, render_template, url_for

from config import Config, db

app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)
app.config.from_object(Config)

db.init_app(app)

# Import models and routes
from models import *
from routes import *

app.register_blueprint(admin_bp)
app.register_blueprint(buyer_bp)
app.register_blueprint(farmer_bp)
app.register_blueprint(auth_bp)

from werkzeug.security import generate_password_hash

with app.app_context():
    db.create_all()
    admin_email = "admin@tmk.com"
    admin_user = User.query.filter_by(email=admin_email).first()
    if not admin_user:
        admin_user = User(
            name="System Admin",
            email=admin_email,
            password_hash=generate_password_hash("admin123"),
            role="admin",
            status="active"
        )
        db.session.add(admin_user)
        db.session.commit()

@app.route("/")
def home():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)