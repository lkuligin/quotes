from flask.ext.wtf import Form
from wtforms import TextField, BooleanField
from wtforms.validators import Required

class NewAssetForm(Form):
	name = TextField('name', validators = [Required()])
	symb = TextField('symb', validators = [Required()])
	source = TextField('source', validators = [Required()])
	#bool = BooleanField('bool', default = False)