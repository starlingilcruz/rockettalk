from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings


@login_required
def chat_view(request, *args, **kwargs):
    return render(request, settings.CHAT_TEMPLATE, {})
