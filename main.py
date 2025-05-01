from importlib.metadata import pass_none, metadata
from wsgiref.handlers import read_environ

import PyPDF2
import os
import pyttsx3
import fitz
from flask import Flask, render_template, flash, request, url_for, redirect
from flask_wtf import FlaskForm
from requests import session
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'
upload_paths = {}

# Form Class
class UploadFileForm(FlaskForm):
    file = FileField("File" , validators=[InputRequired()])
    submit = SubmitField("Upload File")

class ConvertFileForm(FlaskForm):
   convert = SubmitField("Convert File to Audio")

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
        #Store variable in session
        upload_paths['latest'] = save_path
        flash(f"File uploaded successfully to {upload_paths['latest']}, please proceed to convert it. ")
        is_pdf_encrypted()
        is_password_protected()
    return render_template('index.html', form=form, form2=form2)

def is_password_protected():
    doc = fitz.Document(upload_paths['latest'])
    if doc.needs_pass:
        flash (f"The file {doc} need pass.")
    else:
        flash(f"The file doesn't need a pass. ")

def is_pdf_encrypted():
    doc = fitz.Document(upload_paths['latest'])
    if doc.metadata['encryption'] is not None:
        flash (f"The file {doc.metadata['title']} is encrypted by {doc.metadata['encryption']}")
    else:
        flash("The file is not encrypted")

def extract_text():
    text = ""
    if request.method == "POST":
        path = open(upload_paths['latest'], 'rb')
        reader = PyPDF2.PdfReader(path)
        for pages in reader.pages:
            pages_text = pages.extract_text()
            if pages_text:
                text += pages_text
    return text

@app.route('/convert', methods=['GET', 'POST'])
def convert():
    text = extract_text()
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()
    # return redirect(url_for('home'))
    try:
        convert()
    except Exception as e:
        print(f"Error:  {e}")

if __name__ == "__main__":
    app.run(debug=True, port=5001)