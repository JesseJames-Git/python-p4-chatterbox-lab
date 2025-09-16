from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return "Message API"

@app.route('/messages', methods = ['GET', 'POST'])
def messages():
    if request.method == 'GET':
        all_messages = Message.query.order_by(Message.created_at).all()
        message_list = [message.to_dict() for message in all_messages]

        return make_response(jsonify(message_list), 200)
    
    elif request.method == 'POST':
        data = request.get_json()

        new_message = Message(
            body = data["body"],
            username = data["username"]
        )
        db.session.add(new_message)
        db.session.commit()

        return make_response(new_message.to_dict(), 201)


@app.route('/messages/<int:id>', methods = ['PATCH', 'DELETE'])
def messages_by_id(id):

    message = Message.query.filter_by(id=id).first()

    if request.method == 'PATCH':
        data = request.get_json()

        if "body" in data:
            message.body = data["body"]

        db.session.add(message)
        db.session.commit()

        updated_body = message.to_dict()

        return make_response(updated_body, 200)
    
    elif request.method == 'DELETE':

        db.session.delete(message)
        db.session.commit()

        confirm = {"confirmation": " Message has been deleted"}

        return make_response(confirm, 200)

if __name__ == '__main__':
    app.run(port=5555)
