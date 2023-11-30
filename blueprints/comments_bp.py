from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.comment import Comment, CommentSchema
from setup import db
from auth import admin_required

comments_bp = Blueprint('comments', __name__, url_prefix='/<int:card_id>/comments')

# POST /cards/<card_id>/comments

# Create a new comment
@comments_bp.route('/', methods=['POST'])
@jwt_required()
def create_comment(card_id):
    comment_info = CommentSchema(only=['message']).load(request.json)

    comment = Comment(
        message=comment_info['message'],
        user_id = get_jwt_identity(),
        card_id = card_id
    )

    db.session.add(comment)
    db.session.commit()

    return CommentSchema().dump(comment), 201

# Update a Comment
# PUT /cards/<card_id>/comments/<comment_id>

@comments_bp.route('/<int:comment_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_comment(card_id, comment_id):
    comment_info = CommentSchema(only=['message']).load(request.json)
    stmt = db.select(Comment).filter_by(id=comment_id)
    comment = db.session.scalar(stmt)

    if comment:
        comment.message = comment_info.get('message', comment.message)
        db.session.commit()
        return CommentSchema().dump(comment), 200
    
    else:
	    return {'error': 'Comment not found'}, 404

# Delete a Card
@comments_bp.route('/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(card_id, comment_id):
    stmt = db.select(Comment).filter_by(id=comment_id) 
    comment = db.session.scalar(stmt)

    if comment:
        db.session.delete(comment)
        db.session.commit()
        return {'Message': 'Comment successfully deleted'}, 200
    
    else:
	    return {'error': 'Comment not found'}, 404
    



# # Get all cards
# @comments_bp.route('/')
# @jwt_required()
# def all_cards():
#     admin_required()
#     # Select all cards
#     stmt = db.select(Comment) 
#     comments = db.session.scalars(stmt).all()
#     return CardSchema(many=True, exclude=['user.cards']).dump(comments)

# # Get one card
# @comments_bp.route('/<int:id>')
# @jwt_required()
# def one_card(id):
#     stmt = db.select(Card).filter_by(id=id) # .where(Card.id == id)
#     card = db.session.scalar(stmt)
#     if card:
#         return CardSchema().dump(card)
#     else:
# 	    return {'error': 'Card not found'}, 404
