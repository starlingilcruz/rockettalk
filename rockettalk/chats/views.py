from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.http import require_GET

from .store import RedisStore
from .utils import channel_fmt

@login_required
def chat_view(request, *args, **kwargs):
    return render(request, settings.CHAT_TEMPLATE, {})


@require_GET
@login_required
def get_messages(request, *args, **kwargs):
    """ Retrieve messages from channel | group | user """

    channel = kwargs.get("channel", None)
    assert channel, "Error: channel not provided"

    store = RedisStore()
    messages = store.retrieve_objects(hashname=channel_fmt(channel))

    return JsonResponse({'messages': messages})