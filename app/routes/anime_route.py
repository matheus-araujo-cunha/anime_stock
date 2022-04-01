from flask import Blueprint

from app.controllers import anime_controller

bp_animes = Blueprint("animes", __name__, url_prefix="/animes")


bp_animes.post("")(anime_controller.register)
bp_animes.get("")(anime_controller.retrieve)
bp_animes.get("/<int:anime_id>")(anime_controller.get_by_id)
bp_animes.patch("/<int:anime_id>")(anime_controller.update)
bp_animes.delete("/<int:anime_id>")(anime_controller.delete)
