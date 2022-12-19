import re


def split_by_capital_letter(word):
    return list(
        filter(
            lambda w: w != "",
            re.split(r"([A-Z][a-z]+)", word.strip()),
        )
    )


def replace_underscore(word):
    def convert(match_obj):
        if match_obj.group(1):
            return match_obj.group(1)[1].capitalize()

    return re.sub("(_\\w)", convert, word)
