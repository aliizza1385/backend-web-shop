from flask import Flask
from initialize import db
from flask_cors import CORS
from admin.routes import *


app = Flask(__name__)
cors = CORS(app)

app.config.from_object('config.DevConfig') 
db.init_app(app) 





app.register_blueprint(customer_bluprint)
app.register_blueprint(order_blueprint)
app.register_blueprint(product_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(categori_blueprint)
app.register_blueprint(feedbacks_blueprint)
app.register_blueprint(address_blueprint)



from admin.models import *

with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)