from django import forms
from .models import KeyInformation

# 定制关键信息检测表单
class KeyInformationForm(forms.ModelForm):
    class Meta:
        model = KeyInformation
        fields = "__all__"
