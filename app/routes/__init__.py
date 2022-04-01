from flask import Flask, Blueprint
from .anime_route import bp_anime

bp_api = Blueprint("api", __name__, url_prefix="/api")


def init_app(app: Flask):
    bp_api.register_blueprint(bp_anime)
    app.register_blueprint(bp_api)
