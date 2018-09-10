# -*- coding:utf-8 -*-
# Author:YEAR
from django.forms import forms,ModelForm,ValidationError
from myCRM import models
from django.utils.translation import gettext as _

def create_model_form(request,admin_class):
    '''Dynamic create modelformClass'''
    class Meta:
        model=admin_class.model
        fields="__all__"
        # widgets={
        #     '__all__':Textarea()
        # }
        exclude=admin_class.exclude_fields

    def __new__(cls,*args,**kwargs):
        #print(type(cls))
        #print(kwargs)
        #print(cls.base_fields)
        for field_name,field_obj in cls.base_fields.items():
            field_obj.widget.attrs['class']='form-control'
            if kwargs.get('instance',None):
                if field_name in admin_class.readonly_fields:
                    field_obj.widget.attrs['disabled']='disbled'
            if hasattr(admin_class,'clean_%s'%field_name):
                setattr(cls,'clean_%s'%field_name,getattr(admin_class,'clean_%s'%field_name))
        return ModelForm.__new__(cls)

    def custom_clean(self):
        #print('hahahaha--cleanclean')
        error_list=[]
        if admin_class.readonly_table:
            raise ValidationError(_('Readonly Table!!'),code='invalid')
        if self.instance.id:
            for fieldName in admin_class.readonly_fields:
                if type(getattr(self.instance,fieldName)).__name__=="ManyRelatedManager":
                    if set(getattr(self.instance,fieldName).all()) != set(self.cleaned_data.get(fieldName)):
                        error_list.append(ValidationError(_('Readonly field:%(value)s'),code='invalid',params={'value':fieldName}))
                    continue
                if self.cleaned_data.get(fieldName) != getattr(self.instance,fieldName):
                    error_list.append(ValidationError(_('Readonly field:%(value)s'),code='invalid',params={'value':fieldName}))
                #print(self.cleaned_data.get(fieldName),"-----",getattr(self.instance,fieldName))

        if hasattr(admin_class,'custom_form_validation'):
            validationFunc = getattr(admin_class,'custom_form_validation')
            error_list = validationFunc(self,error_list)

        if error_list:
            raise ValidationError(error_list)


    paraDic={'Meta':Meta,'__new__':__new__,'clean':custom_clean}

    _model_form_class= type("DynamicModelForm",(ModelForm,),paraDic)
    print('New Dynamicmodelform Class!!')
    #setattr(_model_form_class,'__new__',__new__)
    return _model_form_class