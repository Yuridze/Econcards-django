
from django import forms

class UploadForm(forms.Form):
    file = forms.FileField(
        label='Файл с карточками (.txt)',
        help_text='Каждая строка: вопрос -> ответ или вопрос\tответ'
    )

    def clean_file(self):
        f = self.cleaned_data['file']
        if f.content_type not in ('text/plain', 'application/octet-stream'):
            raise forms.ValidationError('Загрузите текстовый файл .txt')
        if f.size > 2 * 1024 * 1024:
            raise forms.ValidationError('Файл слишком большой (макс. 2 МБ)')
        return f


class CardForm(forms.Form):
    question = forms.CharField(label='Вопрос', max_length=200, strip=True)
    answer = forms.CharField(label='Ответ', max_length=200, strip=True)

    def clean(self):
        cleaned = super().clean()
        q = cleaned.get('question', '').strip()
        a = cleaned.get('answer', '').strip()
        if not q or not a:
            raise forms.ValidationError('Поля не должны быть пустыми.')
        return cleaned
