from flask import Blueprint, Flask

from .anime_route import bp_animes

bp_api = Blueprint("api", __name__, url_prefix="/api")


def init_app(app: Flask):
    bp_api.register_blueprint(bp_animes)
    app.register_blueprint(bp_api)
