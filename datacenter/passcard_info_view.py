from datacenter.models import Passcard
from datacenter.models import Visit
from datacenter.storage_information_view import format_duration
from datacenter.storage_information_view import is_visit_long
from django.utils import timezone
from django.shortcuts import render
from django.shortcuts import get_object_or_404


def passcard_info_view(request, passcode):
    this_passcard_visits = []
    passcard = get_object_or_404(Passcard, passcode=passcode)
    all_visits = Visit.objects.all()
    for visit in all_visits.filter(passcard=passcard):
        duration = Visit.get_duration(visit)
        suspicion = is_visit_long(duration)
        duration = format_duration(duration)
        entry_time = timezone.localtime(
            visit.entered_at).strftime('%d-%m-%Y %H:%M')
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
