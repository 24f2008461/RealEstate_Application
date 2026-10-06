from flask import Flask,render_template,redirect, request,url_for, session
import os
from datetime import date
from werkzeug.security import generate_password_hash
from config import Config
from models import db,User
from dotenv import load_dotenv
from routes import admin_bp, auth_bp





#Application 
app = Flask(__name__)




# app configs
app.config.from_object(Config)
admin_password = os.environ.get('ADMIN_PASSWORD')
# database initialisation
os.makedirs(os.path.join(os.path.dirname(__file__), "instance"),exist_ok=True)
load_dotenv()
db.init_app(app)

with app.app_context():
    db.create_all()
    if not User.query.filter_by(role='admin').first():
        admin = User(
            username = 'Admin',
            fullname = 'SystemAdmin',
            email = 'systemadmin@realestatedog.com',
            role = 'admin',
            password = generate_password_hash(admin_password),
            phone = '910000000000',
            status = 'approved',
            dob = date(2000,1,1)
        )
        db.session.add(admin)
        db.session.commit()

@app.route('/')
def index():
    if "id" in session:
        role = session.get('role')
        if role == 'admin':
            return redirect('#')
        else:
            return redirect("#")
    return render_template('landing.html')

app.register_blueprint(auth_bp)








if __name__ == "__main__":
    app.run(debug=True)