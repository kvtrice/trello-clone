from setup import db, ma
from datetime import datetime
from marshmallow import fields
from marshmallow.validate import OneOf

VALID_STATUSES = ('To Do', 'In Progress', 'Testing', 'Deployed', 'Done', 'Cancelled')

class Card(db.Model):
    __tablename__ = 'cards'

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(30), default='To Do')
    description = db.Column(db.Text())
    date_created = db.Column(db.Date(), default=datetime.now().strftime('%Y-%m-%d'))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # This is the TABLE name (not the model name) = The table is named 'users', not 'user'. 
    user = db.relationship('User', back_populates='cards')
    comments = db.relationship('Comment', back_populates='card')


class CardSchema(ma.Schema):
    user = fields.Nested('UserSchema', exclude=['password'])
    comments = fields.Nested('CommentSchema', exclude=['card'], many=True)
    status = fields.String(validate=OneOf(VALID_STATUSES))

    class Meta:
        fields = ('id', 'title', 'description', 'status', 'date_created', 'user', 'comments')