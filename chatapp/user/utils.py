from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def group_name(sender, receiver):
    if sender > receiver:
        return f"chat_{sender}{receiver}"
    return f"chat_{receiver}{sender}"

def check_status(user_id,status):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "checkStatus",{"type": "chat.message","id": user_id,"status": status},
    )
