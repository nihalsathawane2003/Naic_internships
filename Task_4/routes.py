from flask import Blueprint, request, jsonify
from database import db, ma
from models import Contact

api = Blueprint("api", __name__)

# Schema for serialization
class ContactSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Contact
        load_instance = True

contact_schema = ContactSchema()
contacts_schema = ContactSchema(many=True)


# Create a contact
@api.route("/contacts", methods=["POST"])
def add_contact():
    data = request.get_json()
    new_contact = Contact(
        name=data["name"],
        email=data["email"],
        phone=data.get("phone")
    )
    db.session.add(new_contact)
    db.session.commit()
    return contact_schema.jsonify(new_contact), 201


# Get all contacts
@api.route("/contacts", methods=["GET"])
def get_contacts():
    all_contacts = Contact.query.all()
    return contacts_schema.jsonify(all_contacts)


# Get a single contact by ID
@api.route("/contacts/<int:id>", methods=["GET"])
def get_contact(id):
    contact = Contact.query.get_or_404(id)
    return contact_schema.jsonify(contact)


# Update a contact
@api.route("/contacts/<int:id>", methods=["PUT"])
def update_contact(id):
    contact = Contact.query.get_or_404(id)
    data = request.get_json()
    
    contact.name = data.get("name", contact.name)
    contact.email = data.get("email", contact.email)
    contact.phone = data.get("phone", contact.phone)
    
    db.session.commit()
    return contact_schema.jsonify(contact)


# Delete a contact
@api.route("/contacts/<int:id>", methods=["DELETE"])
def delete_contact(id):
    contact = Contact.query.get_or_404(id)
    db.session.delete(contact)
    db.session.commit()
    return jsonify({"message": "Contact deleted successfully"}), 200
