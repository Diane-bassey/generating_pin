from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import uuid #to generate a random pin security
import os



# init app object
app = Flask(__name__)


# set up database
app.config["SECRET_KEY"] = "123456KEY"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL") or "sqlite:///database.db"
app.config["DATABASE_TRACK_MODIFITION"] = False

# init db object
db = SQLAlchemy(app)


# create user class
class Users(db.Model):
    __tablename__ = 'users'
    serial_id = db.Column(db.Integer, primary_key = True)
    pin = db.Column(db.String(15), unique=True, nullable=False)

    def __init__(self, pin):
        self.pin = pin
db.create_all()


#route
@app.route("/", methods=["GET"])
def  create_a_pin():
    pin_len = 15
    result = Users(pin=str(uuid.uuid4().int)[0:pin_len])
    db.session.add(result)
    db.session.commit()
    return jsonify({"pin":result.pin, "serial_id":result.serial_id})



# validating a valid pin
@app.route("/pin/<string:serial_id>", methods=["GET"])
def  get_a_pin(serial_id):
    result = Users.query.filter_by(serial_id=serial_id).first()
    if not result:
        return jsonify({"msg":"Invalid pin"})

    return jsonify({"msg":"Valid pin"})



# run server
if __name__ == "__main__":
    app.run(debug=True)
 