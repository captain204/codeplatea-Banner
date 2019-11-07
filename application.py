from flask import(Flask,Blueprint,render_template,redirect,request,flash,url_for,session,logging)
from flask_mysqldb import MySQL
import os
from flask_wtf import FlaskForm
from flask import current_app as app
# from src.models.products.product import Product
from passlib.hash import sha256_crypt
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField,SubmitField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_uploads import UploadSet, IMAGES
from functools import wraps
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = ''
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

mysql = MySQL(app)

app.config['SECRET_KEY'] = 'fjfjkfkjssmdjdjdmdm'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'codepl'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def hompage():
    return render_template("index.html")

class MyForm(FlaskForm):
    firstname = StringField(u'First_Name', validators=[validators.input_required(),validators.Length(min=3, max=50)])
    lastname = StringField(u'Last_Name', validators=[validators.input_required(),validators.Length(min=3, max=50)])
    email = StringField(u'Email', validators=[validators.input_required(),validators.Length(min=3, max=50)])
    stack = StringField(u'Stack', validators=[validators.input_required(),validators.Length(min=3, max=50)])
    image = FileField('Image')
    description = TextAreaField(u'Description', validators=[validators.input_required(),validators.Length(min=3, max=50)])    
    submit = SubmitField('post')

@app.route("/register", methods =['GET','POST'])
def register():
    form = MyForm()
    if form.validate_on_submit():
        firstname = form.firstname.data
        lastname = form.lastname.data
        email = form.email.data
        stack = form.stack.data
        # accessing the file location
        filename = secure_filename(form.image.data.filename)
        image = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        form.image.data.save(image)        
        description = form.description.data
        #  Create Cursor
        cur = mysql.connection.cursor()

        
        verify = cur.execute("SELECT * FROM users WHERE firstname=%s or lastname =%s",(firstname,lastname))

        if verify:
            flash("you already have a banner,double registeration not allowed","danger")
            return redirect(url_for('register'))
          
        else:
                
            # cur.close()
            # execute Query
            cur.execute("INSERT INTO users (firstname, lastname, email, stack, image, description)  VALUES (%s, %s, %s, %s, %s, %s)", (firstname, lastname, email, stack, image, description ))
                        
            # commit to db
            mysql.connection.commit()

            # close connection
            cur.close()

            # flash message
            flash('Thanks for registering, go ahead and print ur banner','success')
            # return redirect('/banner')

    return render_template("register.html",form=form)    
if  __name__ == "__main__":
    app.run(debug=True)
