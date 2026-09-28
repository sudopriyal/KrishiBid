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

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)