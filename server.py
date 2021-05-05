from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from nohttp.auth import login_required

bp = Blueprint("blog", __name__)


@bp.route("/")
@login_required
def index():
    return render_template("blog/base.html")