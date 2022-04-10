from app.exceptions import AnimeInvalidKeysError,MissingKeysError


def validate_keys(correct_keys, anime_keys):
    wrong_fields = [key for key in anime_keys if key not in correct_keys]
  
    if wrong_fields:
        raise AnimeInvalidKeysError(correct_keys, wrong_fields)




def format_date(value):
    return value.strftime("%d/%m/%Y")

def validate_missing_keys(correct_keys, anime_keys):
    missing_keys = [key for key in correct_keys if key not in anime_keys]
    
    if missing_keys:
        raise MissingKeysError(missing_keys,correct_keys)
