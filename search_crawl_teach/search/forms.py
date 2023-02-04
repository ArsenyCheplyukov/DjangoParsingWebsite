import json

from django import forms
from django.core.exceptions import ValidationError

from .models import *


class AddRequestDataForm(forms.Form):
    request_text = forms.CharField(label="Текст запроса", max_length=255)  # verbose_name="Текст запроса"
    num_samples = forms.IntegerField(
        label="Колличество картинок", validators=[MinValueValidator(10), MaxValueValidator(500)]
    )

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    # class Meta:
    #     model = RequestData
    #     fields = ["request_text", "num_samples"]
    #     widgets = {
    #         "request_text": forms.TextInput(attrs={"class": "form-input"}),
    #         "num_samples": forms.NumberInput(attrs={"class": "form-input-slider", min: "10", max: "1000"}),
    #         # "is_published": forms.BooleanField(),  # attrs={"class": "form-input-isprivate"}
    #     }

    def clean_request_text(self):
        request_text = self.cleaned_data["request_text"]
        if len(request_text) > 200:
            raise ValidationError("Длина превышает 200 символов")
        return request_text


class AddModelDataForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields["model_data"].empty_label = "Нет предварительных данных"

    class Meta:
        model = ModelData
        fields = ["type", "request_data"]
        type = forms.ChoiceField(widget=forms.RadioSelect, choices=TYPES)
