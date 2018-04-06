import csv

from reg.models import Participant
from django.utils.crypto import get_random_string

def get_pid():
    allowed_chars       = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    pid_list            = list()

    while True:
        pid = get_random_string(4,allowed_chars)
        if pid not in pid_list:
            pid_list.append(pid)
            break
    return pid

def main():
    """
    Create teams and participants in the database, and link participants with
    their respective teams.
    """

    csv_file            = "attendees.csv"
    team_count          = 0
    participant_count   = 0


    #Delete all existing teams and participants from the database.
    Participant.objects.all().delete()

    with open(csv_file) as f:
        reader = csv.reader(f)
        data = [row for row in reader]

    for item in data:
        p1 = Participant.objects.create(
            participant_id=get_pid(),
            name=item[1].strip(),
            email = item[2].strip(),
            reg_type = item[4].strip(),
            phone=str(item[6]),
        )
    print "{} participants imported.".format(
        participant_count)

main()
