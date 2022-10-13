from datacenter.models import Passcard
from django.shortcuts import render


def active_passcards_view(request):
    all_passcards = Passcard.objects
    context = {
        'active_passcards': all_passcards.filter(is_active=True),
    }
    return render(request, 'active_passcards.html', context)
