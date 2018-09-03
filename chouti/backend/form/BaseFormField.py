# -*- coding:utf-8 -*-
# Author:YEAR

class BaseForm:
    def check_vaild(self,handler):
        flag=True
        value_dict={}
        error_message_dict={}
        success_value_dict={}

        for key,regular in self.__dict__.items():
            input_value=handler.POST.get(key)
            regular.validata(key,input_value)
            if regular.is_valid:
                success_value_dict[key]=regular.value
            else:
                flag=False
                error_message_dict[key]=regular.error
            value_dict[key]=input_value

        return flag,success_value_dict,error_message_dict


class BaseContentFiled:
    REGULAR = ""

    def __init__(self, error_dict=None, required=True):
        self.error_dict = {}
        if error_dict:
            self.error_dict.update(error_dict)
        self.required = required
        self.error = None
        self.is_valid = False
        self.value = None

    def validata(self, name, input_value):
        if not self.required:
            self.is_valid = True
            self.value = input_value
        else:
            if not input_value.strip():
                # self.is_valid=False
                if self.error_dict.get('required', None):
                    self.error = self.error_dict['required']
                else:
                    self.error = "%s is required" % name
            else:
                # 值的验证可以添加在这里
                self.is_valid = True
                self.value = input_value