from flask import Flask, render_template, request, redirect
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sam123'
debug = DebugToolbarExtension(app)

RESPONSES = []

@app.route('/')
def home():
    """Display home page before satisfaction survey & instructions"""
    title = satisfaction_survey.title
    instru = satisfaction_survey.instructions

    return render_template('home.html', title=title, instru=instru)


@app.route('/questions/<int:id>')
def question(id):
    """Display our questions from surveys.py"""
    ques = satisfaction_survey.questions[id]

    return render_template('ques.html', ques=ques, ques_num=id)


@app.route('/answer', methods=['POST'])
def ans():
    # use request to get our choice from the input
    choice = request.form['answer']

    RESPONSES.append(choice)

    return redirect("/questions/<int:id>")