def group_name(sender, receiver):
    if sender > receiver:
        return f"chat_{sender}{receiver}"
    return f"chat_{receiver}{sender}"
