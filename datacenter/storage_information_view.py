from datacenter.models import Visit
from django.shortcuts import render
from django.utils import timezone


def format_duration(duration):
    sec = duration % (24 * 3600)
    hour = sec // 3600
    sec %= 3600
    min = sec // 60
    duration = '%02d:%02d' % (int(hour), int(min))
    return duration


def is_visit_long(visit, minutes=60):
    visiting_time_limit = visit // (minutes * 60)
    if visiting_time_limit:
        return True
    return False


def storage_information_view(request):
    non_closed_visits = []
    people_in_storage = Visit.objects.filter(leaved_at=None)
    for visit in people_in_storage:
        duration = Visit.get_duration(visit)
        suspicion = is_visit_long(duration)
        duration = format_duration(duration)
        entry_time = timezone.localtime(
            visit.entered_at).strftime('%d-%m-%Y %H:%M')
        owner_name = visit.passcard.owner_name
        non_closed_visit = {
                'who_entered': owner_name,
                'entered_at': entry_time,
                'duration': duration,
                'is_strange': suspicion,
        }
        non_closed_visits.append(non_closed_visit)
    context = {
        'non_closed_visits': non_closed_visits,
    }
    return render(request, 'storage_information.html', context)
