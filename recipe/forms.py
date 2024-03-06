from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, IntegerField, SelectField, FileField, TextAreaField, RadioField
from wtforms.validators import DataRequired, Length, Email, ValidationError, Regexp, NumberRange, EqualTo

from recipe.models import User
from flask import session

class LoginForm(FlaskForm): # Login form
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')
	
class SignupForm(FlaskForm): # Sign up form
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[Email()])
	password = PasswordField('Password', validators=[DataRequired(), Regexp("^(?:(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])).{6,16}$", 0, "Must contain A-Z, a-z and 0-9, with 6-16 chars")])
	password2 = PasswordField('Repeat Password', validators=[DataRequired()])
	accept_rules = BooleanField('I accept the site rules', validators=[DataRequired()])
	submit = SubmitField('Register')

	def validate_email(self, field): # Determine whether the mailbox is in use
		u = User.query.filter_by(email=field.data).first()
		if u:
			raise ValidationError('Email is already used')

	def validate_username(self, field): # Determine whether the username is in use
		u = User.query.filter_by(username=field.data).first()
		if u:
			raise ValidationError('Username is already used')

	
class ChangeForm(FlaskForm): # Change password form
	password = PasswordField('Original Password', validators=[DataRequired()])
	newPassword = PasswordField('New Password', validators=[DataRequired(), Regexp("^(?:(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])).{6,16}$", 0, "Must contain A-Z, a-z and 0-9, with 6-16 chars")])
	submit = SubmitField('Submit')

class EditInfoForm(FlaskForm): # Edit personal information
	username = StringField('Name', validators=[DataRequired()])
	detail = StringField('My detail')
	age = IntegerField('Age', validators=[NumberRange(0, 100)])
	gender = StringField('Gender')
	submit = SubmitField('Submit')

	def validate_username(self, field): # Determine whether the username is in use
		u = User.query.filter_by(username=field.data).first()
		if u:
			if u.username != field.data:
				if u:
					raise ValidationError('Username is already used')

class UploadRecipeForm(FlaskForm): # upload recipe
	mat1 = StringField('Materials', render_kw={"class":"mat"})
	dishname = StringField('Name of Recipe', render_kw={"class":"iptone"})
	description = TextAreaField(label="Description", render_kw={"id": "description", "cols":"79", "rows":"12", "placeholder":"Please enter the recipe description","class":"ipttwo"})
	# classify = RadioField("Classify", choices=[("China", "China"), ("South Korean", "South Korean"), ("England", "England"), ("Japan", "Japan")])
	pics = FileField('Photo', render_kw={"onchange":"a(this)", "id":"upload-input", "type":"file", "accept":"image/gif, image/jpg, image/png"})
	step = TextAreaField('Step', render_kw={"style":"height: 258px;", "cols":"45", "rows":"18", "placeholder":"Please enter the procedure description", "class":"sm"})
	submit = SubmitField('Submit')


class AddClassifyForm(FlaskForm): # add classify
	region = StringField('Region', validators=[DataRequired()])
	submit = SubmitField('Submit')

class DeleteClassifyForm(FlaskForm):
	submit = SubmitField('Submit')
