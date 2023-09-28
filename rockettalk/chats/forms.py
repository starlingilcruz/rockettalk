from django import forms


class ChatMessageForm(forms.Form):
    # sender = forms.CharField(max_length=50)
    username = forms.CharField(max_length=50)
    message = forms.CharField(max_length=180)
