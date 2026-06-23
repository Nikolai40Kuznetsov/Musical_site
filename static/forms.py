from django import forms

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result

class New_Article(forms.Form):
    article_title = forms.CharField(max_length=20, label="Заголовок статьи")
    article_annotation = forms.CharField(max_length=200, label="Аннотация")
    article_preview_image = forms.ImageField(label="Превью")
    article_text = forms.CharField(widget=forms.TextInput, label="Текст статьи")
    article_pictures = MultipleFileField(label="Картинки в статье")


    