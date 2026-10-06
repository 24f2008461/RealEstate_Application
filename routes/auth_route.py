
#Autherization Route
from flask import session, redirect, render_template, request, url_for,Blueprint,flash
from werkzeug.security import generate_password_hash, check_password_hash
from autherization import isLoggedIn, role_validate
from models import User,db


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login" , methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        pass
    return render_template("/auth/login.html")


@auth_bp.route("/register", methods=['GET','POST'])
def register():
    if request.method=='POST':
        fname = request.form.get('fullname','').strip()
        uname = request.form.get('username','').strip()
        email = request.form.get('email','').strip()
        phone = request.form.get('phone','').strip()
        dob = request.form.get('dob','')
        password = request.form.get('password')

        if not fname or not uname or not email or not phone or not dob or not password:
            flash('Please fill all the required field to get registerd.' ,'warning')
            return redirect(url_for('auth.register'))

        if len(fname) <= 3 or len(uname) <= 3:
            flash('Username or Fullname must have 4 characters.', 'warning')
            return redirect(url_for('auth.register'))

        if '@' or '.' not in email:
            flash('Please provide a vaild email address.', 'danger')
            return redirect(url_for('auth.register'))
        
        if len(phone) < 10 or not phone.isdigit():
            flash("Phone number is not valid.", 'danger')
            return redirect(url_for('auth.register'))

        if len(password) < 5 :
            flash("Password must have 5 characters.", 'danger')
            return redirect(url_for('auth.register'))

        if User.query.filter_by(username=uname).first():
            flash("Username already exits, Please try another.",'warning')
            return redirect(url_for('auth.register'))

        new_user = User(
            username=uname,
            fullname=fname,
            email=email,
            phone=phone,
            dob=dob,
            password=generate_password_hash(password=password)

        )      

        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("/auth/register.html")
