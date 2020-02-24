import os
from django.core.exceptions import ValidationError
from datetime import date


def validate_start_date(value):
    ext = value  # [0] returns path+filename
    today = date.today()
    if ext <= today:
        raise ValidationError('Starting date should be equal or grater than todays date.')


def validate_start_end_date(value):
    ext = value  # [0] returns path+filename
    today = date.today()
    if ext <= today:
        raise ValidationError('Ending date should be greater than start date.')
