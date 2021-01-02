import time

# Gets the Nicknames of people


def get_user_nickname(user_id):
    sammy = ["sammy", "fatzkes"]
    julian = ["julian"]
    max = ["max"]
    niclas = ["niclas", "nici"]
    thorsten = ["thorsten", "0013"]

    user_id_dict = {}


# Initalizes time for timed functions


def get_time():
    actual = datetime.datetime.now()
    actual_time = f"{actual.hour}:{actual.minute}:{actual.second}"
    actual_date_time = f"{actual.day}.{actual.month}.{actual.year} at {actual_time}"
    return actual_time, actual_date_time