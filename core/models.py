from django.db import models
from django.core.exceptions import ValidationError
import re


class Student(models.Model):
    serial_no = models.IntegerField(unique=True)
    batch = models.CharField(max_length=10)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email_id = models.EmailField()
    contact = models.CharField(max_length=15)


def validate_contact(value):
    try:
        value = str(int(value))
        regex = '^(?:(?:\+|0{0,2})91(\s*[\ -]\s*)?|[0]?)?[789]\d{9}|(\d[ -]?){10}\d$'
        if re.search(regex, value):
            return True
        else:
            return False
    except:
        return False


def validate_emailid(value):
    if re.match(r'\b[\w.-]+@[\w.-]+.\w{2,4}\b', value):
        return True
    else:
        return False