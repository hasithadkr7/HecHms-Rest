from flask import Flask
import os
from flask_json import FlaskJSON
from flask_uploads import UploadSet, configure_uploads

UPLOADS_DEFAULT_DEST = '/home/uwcc-admin/udp_150/hec-hms'

app = Flask(__name__)
flask_json = FlaskJSON()
# upload set creation
model_hec = UploadSet('modelHec', extensions='csv')


db_config = {
    'connector': 'pymysql',
    'host': "104.198.0.87",
    'port': 3306,
    'user': "curw_user",
    'password': "curw",
    'db': "curw"
}

sqlalchemy_config = {
    'db_url': "mysql+%s://%s:%s@%s:%d/%s" % (db_config['connector'], db_config['user'], db_config['password'],
                                             db_config['host'], db_config['port'], db_config['db'])
}


def create_app(db):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = sqlalchemy_config['db_url']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOADS_DEFAULT_DEST'] = os.path.join(UPLOADS_DEFAULT_DEST, 'hec_hms')
    app.config['UPLOADED_FILES_ALLOW'] = 'csv'
    configure_uploads(app, model_hec)
    flask_json.init_app(app)
    return app, db