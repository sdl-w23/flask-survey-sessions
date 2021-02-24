from flask import Flask, request, render_template, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey


app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"

debug = DebugToolbarExtension(app)




@app.route("/")
def show_survey():
    return render_template("survey_page.html", survey=satisfaction_survey)

@app.route("/start", methods=["POST"])
def to_survey():
    """ Redirect to the first question. """
    session["responses"] = []
    return redirect("/questions/0")

@app.route("/questions/<int:qnum>")
def show_question(qnum):
    responses = session.get("responses")

    if(qnum > len(satisfaction_survey.questions)):
        flash(f"Invalid question ({qnum})!")
        return redirect(f"/questions/{len(responses)}")

    question = satisfaction_survey.questions[qnum]
    
    if(responses is None):
        return redirect("/")

    if(qnum != len(responses)):
        flash(f"Invalid question ({qnum})!")
        return redirect(f"/questions/{len(responses)}")
    
    if(len(responses) == len(satisfaction_survey.questions)):
        return redirect("/end")

    return render_template("question_page.html", question_num = qnum, question=question)

@app.route("/answer", methods=["POST"])
def whats_next():
    choice = request.form['choices']
    responses = session["responses"]
    responses.append(choice)
    session["responses"] = responses

    if(len(responses) == len(satisfaction_survey.questions)):
        return redirect("/end")
    else:
        return redirect(f"/questions/{len(responses)}")
    

@app.route("/end")
def end():
    return render_template("end.html")
    