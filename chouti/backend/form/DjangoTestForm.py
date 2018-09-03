# -*- coding:utf-8 -*-
# Author:YEAR
from . import BaseFormField
from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets
from django.forms import fields
from django.forms import models as models_fields
from django.core.validators import RegexValidator
from chouti import models
import json

class JsonCustomerEncoder(json.JSONEncoder):
    def default(self, field):
        if isinstance(field,ValidationError):
            return {'code':field.code,'message':field.message}
        else:
            return json.JSONEncoder.default(self,field)


class DjTestForm(forms.Form):
    t1=forms.CharField(required=True,
                       label='name',
                       widget=widgets.TextInput(attrs={'class':'t1','placeholder':'username'}),
                       show_hidden_initial=True,
                       initial='biubiu',
                       validators=[RegexValidator(r'^[0-9]+$','pls input number',code='number')],
                       disabled=False,
                       label_suffix=':',
                       max_length=8,
                       min_length=2,
                       strip=True,
                       error_messages={'required':'not null','invalid':'format error','number':'must number','max_length':'too long'})
    t2=forms.ChoiceField(choices=[(1,'hehe'),(2,'haha')])
    t3=forms.IntegerField(widget=widgets.Select(choices=[])) #自动做类型转换
    #t4=forms.FileField()
    t4=models_fields.ModelChoiceField(queryset=models.News.objects.all(),empty_label='Pls choose',to_field_name='id')
    t5=forms.TypedChoiceField(
        choices=[(1,'hehe'),(2,'biubiu'),],
        initial=2,
        coerce=lambda x:int(x)
    )
    t6=forms.FilePathField(path='chouti/static',
                           allow_folders=True,
                           recursive=True)

    def __init__(self,*args,**kwargs):
        super(DjTestForm,self).__init__(*args,**kwargs)
        self.fields['t3'].widget.choices=models.News.objects.all().values_list('id','title')

class DjTestModelForm(forms.ModelForm):
    class Meta:
        model = models.News
        fields= '__all__'