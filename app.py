from flask import Flask, render_template, request, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

SESSION_KEY = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sam123'
debug = DebugToolbarExtension(app)

@app.route('/start', methods=['POST'])
def start():
    """Reset our cookies"""
    session[SESSION_KEY] = []

    return redirect('/questions/0')

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

    # use our session's list to keep trace of the user's choices
    user_answers = session[SESSION_KEY]
    user_answers.append(choice)

    # was stuck on the same question, this allows us to continue to the
    # next question
    session[SESSION_KEY] = user_answers

    if (len(user_answers) == len(satisfaction_survey.questions)):
        return redirect("/done")
    else:
        return redirect(f"/questions/{len(user_answers)}")


@app.route('/done')
def done():
    """Show completed survey screen"""
    return render_template('done.html')