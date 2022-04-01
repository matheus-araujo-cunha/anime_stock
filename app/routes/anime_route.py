from flask import Blueprint
from app.controllers import anime_controller

bp_anime = Blueprint("anime", __name__, url_prefix="/animes")


bp_anime.post("")(anime_controller.register)
bp_anime.get("")(anime_controller.retrieve)
bp_anime.get("/<int:anime_id>")(anime_controller.get_by_id)
bp_anime.patch("/<int:anime_id>")(anime_controller.update)
bp_anime.delete("/<int:anime_id>")(anime_controller.delete)
