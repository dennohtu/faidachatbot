from flask import Flask, render_template, request
from wtforms import Form, StringField, validators
from chat_bot import Faida

app = Flask(__name__)
trained = Faida()
chats = []

class ChatForm(Form):
    message = StringField('Write Message', [validators.DataRequired(),
     validators.length(min=2)])
 
@app.route('/', methods=['GET', 'POST'])
def index():
    form = ChatForm(request.form)
    if request.method == 'POST' and form.validate():
        message = form.message.data
        result = trained.chat_gui(message)
        chat = {}
        chat["faida"] = result
        chat["user"] = message
        chats.append(chat)
    return render_template("home.html", form=form, chats=chats)

if(__name__ == '__main__'):
    app.run()