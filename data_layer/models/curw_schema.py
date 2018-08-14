from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Note:
# The table name is automatically set for you unless overridden. It’s derived from the class name converted to
# lowercase and with “CamelCase” converted to “camel_case”.
# To override the table name, set the_tablename_class attribute.


class Data(db.Model):
    id = db.Column(db.VARCHAR(64), nullable=False, primary_key=True)
    time = db.Column(db.DATETIME, nullable=False, primary_key=True)
    value = db.Column(db.DECIMAL(8, 3), nullable=False)
    __tablename__ = 'data'

    def __repr__(self):
        return '<Data %r %r %r>' % (self.id, self.time, self.value)


class Run(db.Model):
    id = db.Column(db.VARCHAR(64), nullable=False, primary_key=True)
    name = db.Column(db.VARCHAR(255), nullable=False)
    start_date = db.Column(db.DATETIME)
    end_date = db.Column(db.DATETIME)
    station = db.Column(db.INT, nullable=False)
    variable = db.Column(db.INT, nullable=False)
    unit = db.Column(db.INT, nullable=False)
    type = db.Column(db.INT, nullable=False)
    source = db.Column(db.INT, nullable=False)
    __tablename__ = 'run'

    def __repr__(self):
        return '<RunView %r %r %r %r %r %r %r>' % \
               (self.id, self.name, self.station, self.variable, self.unit, self.type, self.source)

class RunView(db.Model):
    id = db.Column(db.VARCHAR(64), nullable=False, primary_key=True)
    name = db.Column(db.VARCHAR(255), nullable=False)
    start_date = db.Column(db.DATETIME)
    end_date = db.Column(db.DATETIME)
    station = db.Column(db.VARCHAR(45), nullable=False)
    variable = db.Column(db.VARCHAR(100), nullable=False)
    unit = db.Column(db.VARCHAR(10), nullable=False)
    type = db.Column(db.VARCHAR(45), nullable=False)
    source = db.Column(db.VARCHAR(45), nullable=False)
    __tablename__ = 'run_view'

    def __repr__(self):
        return '<RunView %r %r %r %r %r %r %r>' % \
               (self.id, self.name, self.station, self.variable, self.unit, self.type, self.source)
