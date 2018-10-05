from flask import Flask
from flask_restful import Api
from src.Resource.Display import cis, duty, headlines, intervention

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/permaalert?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)

api.add_resource(cis.CIS, '/display/cis/<string:location>')
api.add_resource(duty.Duty, '/display/cis/<string:location>/duties/<string:engine>')
api.add_resource(intervention.Intervention, '/display/cis/<string:location>/intervention')
api.add_resource(headlines.Headlines, '/display/headlines')


if __name__ == '__main__':

    # Initialize DB
    from src.common.db import db
    db.init_app(app)

    app.run(debug=True)

