from django.db import models
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


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    @staticmethod
    def get_duration(visit):
        entered_at = timezone.localtime(visit.entered_at)
        leaved_at = timezone.localtime(visit.leaved_at)
        duration = leaved_at - entered_at
        return duration.total_seconds()

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )
