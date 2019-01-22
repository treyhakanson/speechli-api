from flask import Blueprint, render_template


base_bp = Blueprint("base_bp", __name__)


@base_bp.route("/", methods=["GET"])
def home():
    return render_template("base/index.html")
