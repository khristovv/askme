from django import forms
from questions.models import Answer


class PostQuestionForm(forms.Form):
    question_text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 2,
                "placeholder": "What's up ??"
            }
        ),
        max_length=512,
        label="Ask",
    )

    is_anonymous = forms.BooleanField(
        required=False,
        label="Ask anonymously"
    )


class AnswerQuestionForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                "rows": 2,
                "id": "id_answer_content"})
        }


