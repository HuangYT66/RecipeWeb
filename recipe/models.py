from datetime import datetime
from recipe import db

class User(db.Model):
	# User database
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	age = db.Column(db.Integer())
	gender = db.Column(db.String(64))
	detail = db.Column(db.String(64))

	def __repr__(self):
		return '<User {}>'.format(self.username)

class Recipe(db.Model):
	# all recipe database
	name = db.Column(db.String(128), primary_key=True)
	region = db.Column(db.String(128), db.ForeignKey("classify.region", ondelete='CASCADE'))
	image = db.Column(db.String(128))
	description = db.Column(db.String)
	author = db.Column(db.String(128))

	def __repr__(self):
		return '<recipe {}>'.format(self.name)

class steps(db.Model):
	# all steps
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(128), db.ForeignKey("recipe.name", ondelete='CASCADE'))
	order = db.Column(db.Integer)
	step = db.Column(db.String(128))
	image = db.Column(db.String(128))

	def __repr__(self):
		return '<steps {}>'.format(self.name)


class materials(db.Model):
	# all materials
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(128), db.ForeignKey("recipe.name", ondelete='CASCADE'))
	order = db.Column(db.Integer)
	material = db.Column(db.String(128))

	def __repr__(self):
		return '<materials {}>'.format(self.name)


class Classify(db.Model):
	# classify database
	region = db.Column(db.String(128), primary_key=True)
	image = db.Column(db.String(128))

	def __repr__(self):
		return '<classify {}>'.format(self.name)

class Log(db.Model):
	# log messages database
	id = db.Column(db.Integer, primary_key=True, nullable=False)
	description = db.Column(db.String)
	type = db.Column(db.String)

	def __repr__(self):
		return '<Log {}>'.format(self.name)

class Collections(db.Model):
	# collections database
	id = db.Column(db.Integer, primary_key=True, nullable=False)
	recipe = db.Column(db.String, db.ForeignKey("recipe.name", ondelete='CASCADE'))
	username = db.Column(db.String, db.ForeignKey("user.username", ondelete='CASCADE', onupdate='CASCADE'))

	def __repr__(self):
		return '<Collections {}>'.format(self.name)