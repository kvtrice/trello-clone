from flask import abort
from flask_jwt_extended import get_jwt_identity
from models.user import User
from setup import db

def admin_required():
    # 1. Get the identity from the token
    user_id = get_jwt_identity()

    # 2. Retrieve the user that has that email address
    stmt = db.select(User).filter_by(id = user_id)
    user = db.session.scalar(stmt)

    # 3. Check if this user has is_admin == True
    if not (user and user.is_admin):
        abort(401)