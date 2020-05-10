from django import forms


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


