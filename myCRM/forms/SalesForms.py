# -*- coding:utf-8 -*-
# Author:YEAR
from django.forms import ModelForm
from myCRM import models

class EnrollmentForm(ModelForm):
    class Meta:
        model=models.Enrollment
        fields=['customer','enrolled_class','consulant']


    def __new__(cls, *args, **kwargs):
        for field_name,field_obj in cls.base_fields.items():
            field_obj.widget.attrs['class']='form-control'
            if field_name=='customer':
                field_obj.widget.attrs['readonly']='readonly'
        return super(EnrollmentForm,cls).__new__(cls)

