from http import HTTPStatus


class AnimeNotFound(Exception):
    def __init__(self, anime_id):
        self.message = f"Anime ID {anime_id} not found"
        self.status_code = HTTPStatus.NOT_FOUND


class AnimeInvalidKeysError(Exception):
    def __init__(self, available_keys, wrong_keys_sended):
        self.available_keys = list(available_keys)
        self.wrong_keys_sended = wrong_keys_sended
        self.status_code = HTTPStatus.UNPROCESSABLE_ENTITY

class MissingKeysError(Exception):
    def __init__(self,missing_keys,correct_keys):
        self.missing_keys = missing_keys
        self.correct_keys = correct_keys
        self.status_code = HTTPStatus.BAD_REQUEST