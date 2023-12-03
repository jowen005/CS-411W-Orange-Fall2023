from django.core.management import call_command


def driver():
    call_command('manualTrends')
