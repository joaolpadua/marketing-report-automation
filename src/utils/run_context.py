import datetime


def generate_run_id():

    now = datetime.datetime.utcnow()

    return now.strftime("run_%Y_%m_%d_%H%M")