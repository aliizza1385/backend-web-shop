from flask import Flask,jsonify
from initialize import *
from flask_cors import CORS
from admin.routes import *
from customer_viwe.route import *

app = Flask(__name__)
cors = CORS(app)

app.config.from_object('config.DevConfig') 
login_manager.init_app(app)
db.init_app(app) 

app.register_blueprint(customer_bluprint)
app.register_blueprint(shop)
app.register_blueprint(login)
app.register_blueprint(customer_viwe)
app.register_blueprint(order_blueprint)
app.register_blueprint(product_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(categori_blueprint)
app.register_blueprint(feedbacks_blueprint)
app.register_blueprint(address_blueprint)
app.register_blueprint(payments_blueprint)
app.register_blueprint(login_admin)
app.register_blueprint(log_blueprint)
app.register_blueprint(kpi_blueprint)
app.register_blueprint(customer)



from admin.models import *

with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)