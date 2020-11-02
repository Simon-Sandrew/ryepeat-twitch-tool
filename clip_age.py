import datetime

def find_clip_age(hours_since_created):
    converted = int(hours_since_created)
    d = datetime.datetime.utcnow()
    subtract = datetime.timedelta(hours=converted)
    time2 = d-subtract
    finished = time2.isoformat("T") + "Z"
    return finished
