from flask import Flask, render_template, redirect, request
import json
import datetime
import pytz
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
import os
from werkzeug.utils import secure_filename
from instabot import Bot

app = Flask(__name__)
app.config['SECRET_KEY'] = 'MYSecretKey'
app.config['UPLOAD_FOLDER'] = 'static/files'

class UploadFileForm(FlaskForm):
    file = FileField("File")
    submit = SubmitField("Upload File")

bot = Bot()

bot.login(
    username = "koala_hugger516", 
    password = "y3o4-8_5dCE0$Tf"
)

users=["snickers983"]
text="New Message"

@app.route("/")
def home():
    with open('data/together.json', 'r') as admin_file:
        admin_dict=json.load(admin_file)
    
    
    return render_template('index.html', admin = admin_dict, name = "Jeff")

@app.route('/wendy/post', methods=["GET", "POST"])
def post():
    form = UploadFileForm()
    if request.method == "GET":
        return render_template("post.html", name = 'Wendy', form = form)
    
    if request.method == "POST":
        today = datetime.datetime.now(pytz.timezone('US/Pacific'))
        with open('data/together.json', 'r') as wendy_file:
            wendy_dict=json.load(wendy_file)
        new_post = request.form.get('post-input')
        file = form.file.data
        
        try:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))

            image_path=secure_filename(file.filename)
        except:
            image_path=""
        #new_embed = request.form.get('embed')
        new_date = today.strftime("%b-%d-%Y %I:%M %p")
        new_dict={
            "name": "Wendy",
            "post": new_post,
            "date": new_date,
            "img":  image_path,
            "embed": ""
        }
        wendy_dict.insert(0, new_dict)
        

        

        bot.send_message(new_post, users)

        with open('data/together.json', 'w') as wendy_file:
            wendy_file.write(json.dumps(wendy_dict[:30], indent=4))
        return redirect('/')
    return redirect('/')


@app.route('/jeff/post', methods=["GET", "POST"])
def postAdmin():
    form = UploadFileForm()
    if request.method == "GET":
        return render_template("post.html", name = 'Jeff', form = form)
    
    if request.method == "POST":
        today = datetime.datetime.now(pytz.timezone('US/Pacific'))
        with open('data/together.json', 'r') as admin_file:
            admin_dict=json.load(admin_file)
        new_post = request.form.get('post-input')
        
        
        file = form.file.data
        try:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))

            image_path=secure_filename(file.filename)
        except:
            image_path=""
        new_embed = request.form.get('embed')
        new_date = today.strftime("%b-%d-%Y %I:%M %p")       
        new_dict={
            "name": "Jeff",
            "post": new_post,
            "date": new_date,
            "img": image_path,
            "embed": new_embed
        }
        admin_dict.insert(0, new_dict)

        
        with open('data/together.json', 'w') as wendy_file:
            wendy_file.write(json.dumps(admin_dict[:30], indent=4))
        return redirect('/')
    return redirect('/')



# @app.route('/wendy')
# def wendy():
#     with open('data/wendy.json', 'r') as wendy_file:
#         wendy_dict=json.load(wendy_file)
#     return render_template('index.html', wendy=wendy_dict, name='Wendy')



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
