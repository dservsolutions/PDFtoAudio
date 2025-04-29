from importlib.metadata import pass_none

import PyPDF2
import pyttsx3
from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'

# Form Class
class UploadFileForm(FlaskForm):
    file = FileField("File" , validators=[InputRequired()])
    submit = SubmitField("Upload File")

class ConvertFileForm(FlaskForm):
   convert = SubmitField("Convert File to Audio")

# def convert(file):
#     path = open(file, 'rb')
#     pdfreader = PyPDF2.PdfFileReader(path)
#
#     from_page = pdfreader.getPage(1)
#     text = from_page.extractText()
#
#     # Reading the text
#     speak = pyttsx3.init()
#     speak.say(text)
#     speak.runAndWait()

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods = ['GET', 'POST'])
def home():
    form = UploadFileForm()
    form2 = ConvertFileForm()
    if form.validate_on_submit():
        file = form.file.data # First grab the file
        filename = secure_filename(file.filename)
        save_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], filename) # Then save the file
        file.save(save_path)
        flash("File uploaded successfully, please proceed to convert it.  ")
    return render_template('index.html', form=form, form2=form2)

if __name__ == "__main__":
    app.run(debug=True, port=5001)