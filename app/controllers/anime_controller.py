from http import HTTPStatus

from flask import jsonify, request
from psycopg2.errors import UndefinedTable, UniqueViolation

from app.exceptions import AnimeInvalidKeysError, AnimeNotFound
from app.models.anime_model import Anime
from app.services import validate_keys, format_date


def retrieve():
    try:
        list_animes = Anime.get_all()
    except UndefinedTable:
        return {"data": []}

    for anime in list_animes:
        anime.update({"released_date": format_date(anime["released_date"])})

    return {"data": list_animes}, HTTPStatus.OK


def get_by_id(anime_id: int):
    try:
        anime = Anime.get_anime_by_id(anime_id)
    except AnimeNotFound or UndefinedTable as error:
        return {"error": error.message}, error.status_code
    anime.update({"released_date": format_date(anime["released_date"])})
    return {"data": [anime]}, HTTPStatus.OK


def register():
    data = request.get_json()
    try:
        anime = Anime(**data)
        registered_anime = anime.register_item()
    except UndefinedTable:
        Anime.create_or_check_table()
        registered_anime = anime.register_item()
    except AnimeInvalidKeysError as error:
        return {
            "available_keys": error.available_keys,
            "wrong_keys_sended": error.wrong_keys_sended,
        }, error.status_code
    except UniqueViolation as error:
        return {
            "error": f"Anime {anime.anime} is already exists"
        }, HTTPStatus.UNPROCESSABLE_ENTITY
    registered_anime.update(
        {"released_date": format_date(registered_anime["released_date"])}
    )
    return jsonify(registered_anime), HTTPStatus.CREATED


def update(anime_id: int):
    try:
        data = request.get_json()
        validate_keys(Anime.FIELDNAMES, data)
        updated_anime = Anime.update_item(anime_id, data)
    except AnimeNotFound or UndefinedTable as error:
        return {"error": error.message}, error.status_code
    except AnimeInvalidKeysError as error:
        return {
            "available_keys": error.available_keys,
            "wrong_keys_sended": error.wrong_keys_sended,
        }, error.status_code
    except UniqueViolation:
        return {
            "error": f"Anime {data['anime']} is already exists"
        }, HTTPStatus.UNPROCESSABLE_ENTITY
    updated_anime.update(
        {"released_date": format_date(updated_anime["released_date"])}
    )
    return {"data": updated_anime}, HTTPStatus.OK


def delete(anime_id: int):

    try:
        Anime.delete_item(anime_id)
    except AnimeNotFound or UndefinedTable as error:
        return {"error": error.message}, error.status_code

    return {}, HTTPStatus.NO_CONTENT
