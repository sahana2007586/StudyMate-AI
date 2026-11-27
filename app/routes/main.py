from flask import Blueprint, render_template


main = Blueprint("main", __name__)


@main.route("/")
def home():
    """Render the StudyMate AI landing page."""
    return render_template("index.html")
