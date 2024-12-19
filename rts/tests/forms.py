from django import forms
from .models import Test


class TestCreationForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['title', 'description', 'category', 'difficulty',
                  'duration', 'attempts_allowed', 'is_published']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'duration': forms.NumberInput(attrs={'min': 1}),
            'attempts_allowed': forms.NumberInput(attrs={'min': 1}),
        }

    def __init__(self, *args, **kwargs):
        self.owner = kwargs.pop('owner', None)
        super().__init__(*args, **kwargs)

        # Добавляем поля для вопросов (динамически)
        self.fields['question_count'] = forms.IntegerField(
            min_value=1,
            initial=1,
            label='Количество вопросов',
            widget=forms.NumberInput(attrs={'id': 'question_count'})
        )

    def clean(self):
        cleaned_data = super().clean()
        if not self.owner:
            raise forms.ValidationError('Владелец теста должен быть указан')
        return cleaned_data

    def save(self, commit=True):
        test = super().save(commit=False)
        if self.owner:
            test.owner = self.owner

        # Структура теста будет заполняться через JavaScript
        test.test = {
            'questions': []  # Будет заполнено через AJAX
        }

        if commit:
            test.save()
        return test


class TestQuestionForm(forms.Form):
    """Форма для отдельного вопроса (будет использоваться через JavaScript)"""
    question_text = forms.CharField(
        label='Текст вопроса',
        widget=forms.Textarea(attrs={'rows': 2})
    )
    answer_type = forms.ChoiceField(
        label='Тип ответа',
        choices=[
            ('single', 'Один правильный ответ'),
            ('multiple', 'Несколько правильных ответов'),
            ('text', 'Текстовый ответ')
        ]
    )
    points = forms.IntegerField(
        label='Баллы за вопрос',
        min_value=1,
        initial=1
    )