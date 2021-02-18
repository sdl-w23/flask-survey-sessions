from flask import Flask, request, render_template
from flask_debugtoolbar import DebugToolbarExtension
from stories import story

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"

debug = DebugToolbarExtension(app)

@app.route('/')
def show_form():
    """Show the form for MadLibs."""
    prompts = story.prompts
    return render_template("questions.html", prompts=prompts)

@app.route("/story")
def story_time():
    """Tell the story."""

    text = story.generate(request.args)

    return render_template("story.html", text=text)