from .. import db, flask_bcrypt

class VadrRun(db.Model):
   run_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   process_id = db.Column(db.Integer, nullable=False)
   sequence_name = db.Column(db.String(700), nullable=False)
   sequence = db.Column(db.String(40000), nullable=False)
   status = db.Column(db.String(15), nullable=False)
   registered_on = db.Column(db.DateTime, nullable=False)