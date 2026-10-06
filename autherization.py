from flask import session, redirect, flash, url_for
from functools import wraps


def isLoggedIn(func):
    @wraps(func)
    def wrapper(*a, **kw):
        if 'id' not in session:
            flash("Please Log in to your account first!",'warning')
            return redirect("#")
        return func(*a,**kw)
    return wrapper

def role_validate(*roles):
    def wrapper(func):
        @wraps(func)
        @isLoggedIn
        def decorated(*a,**kw):
            if session.get('role') not in roles:
                flash("Invalid UserType! Accesss Forbidden",'danger')
                return redirect(url_for("#"))
            return func(*a,**kw)
        return decorated
    return wrapper



