from app.exceptions import AnimeInvalidKeysError


def validate_keys(correct_keys, anime_keys):
    wrong_fields = [key for key in anime_keys if key not in correct_keys]

    if wrong_fields:
        raise AnimeInvalidKeysError(correct_keys, wrong_fields)


def format_date(value):
    return value.strftime("%d/%m/%Y")
