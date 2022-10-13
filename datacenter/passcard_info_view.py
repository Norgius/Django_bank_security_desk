from datacenter.models import Passcard, Visit
from datacenter.models import format_duration, is_visit_long
from django.utils import timezone
from django.shortcuts import render, get_object_or_404


def passcard_info_view(request, passcode):
    this_passcard_visits = []
    passcard = get_object_or_404(Passcard, passcode=passcode)
    all_person_visits = Visit.objects.filter(passcard=passcard)
    for visit in all_person_visits:
        duration = Visit.get_duration(visit)
        suspicion = is_visit_long(duration)
        duration = format_duration(duration)
        entry_time = timezone.localtime(visit.entered_at)
        this_passcard_visit = {
                'entered_at': entry_time,
                'duration': duration,
                'is_strange': suspicion
        }
        this_passcard_visits.append(this_passcard_visit)
    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
