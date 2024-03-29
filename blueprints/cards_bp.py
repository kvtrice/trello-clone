from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.card import Card, CardSchema
from setup import db
from auth import admin_required, authorize
from blueprints.comments_bp import comments_bp

cards_bp = Blueprint('cards', __name__, url_prefix='/cards')

# Get all cards
@cards_bp.route('/')
@jwt_required()
def all_cards():
    admin_required()
    # Select all cards
    stmt = db.select(Card) #.where(db.or_(Card.status != 'Done', Card.id > 2)).order_by(Card.title.desc())
    cards = db.session.scalars(stmt).all()
    return CardSchema(many=True, exclude=['user.cards']).dump(cards)

# Get one card
@cards_bp.route('/<int:id>')
@jwt_required()
def one_card(id):
    stmt = db.select(Card).filter_by(id=id) # .where(Card.id == id)
    card = db.session.scalar(stmt)
    if card:
        return CardSchema().dump(card)
    else:
	    return {'error': 'Card not found'}, 404
    
# Create a new card
@cards_bp.route('/', methods=['POST'])
@jwt_required()
def create_card():
    # Parse incoming POST body through Schema
    card_info = CardSchema(exclude=['id', 'date_created']).load(request.json)

    card = Card(
        title=card_info['title'],
        description=card_info.get('description', ''),
        status=card_info.get('status', 'To Do'),
        user_id = get_jwt_identity()
    )

    db.session.add(card)
    db.session.commit()

    return CardSchema().dump(card), 201

# Update a Card
@cards_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_card(id):
    card_info = CardSchema(exclude=['id', 'date_created']).load(request.json)
    stmt = db.select(Card).filter_by(id=id) # .where(Card.id == id)
    card = db.session.scalar(stmt)

    if card:
        authorize(card.user_id)
        card.title = card_info.get('title', card.title)
        card.description = card_info.get('description', card.description)
        card.status = card_info.get('status', card.status)

        db.session.commit()

        return CardSchema().dump(card), 200
    
    else:
	    return {'error': 'Card not found'}, 404

# Delete a Card
@cards_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_card(id):
    admin_required()
    stmt = db.select(Card).filter_by(id=id) # .where(Card.id == id)
    card = db.session.scalar(stmt)

    if card:
        db.session.delete(card)
        db.session.commit()
        return {'Message': 'Card successfully deleted'}, 200
    
    else:
	    return {'error': 'Card not found'}, 404

# Register the comments blueprint
cards_bp.register_blueprint(comments_bp)

