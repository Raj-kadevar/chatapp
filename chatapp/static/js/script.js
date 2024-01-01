
$('.chat-message-submit').click(function(e) {
    event.preventDefault();
    message = $('#txtArea').val();
    chatSocket.send(JSON.stringify({
        'message': message
    }));
    $('#txtArea').val('');
});

function senderDiv(message) {
    return ('<li class="d-flex justify-content-between mb-4 user-chat sender">' +
        '<div class="card mask-custom ">' +
        '<div class="card-body">' +
        '<p class="mb-0">' +
        ' ' + message + '' +
        '</p>' +
        '</div>' +
        '</div>' +
        '</li></br>')
}

function receiverDiv(message) {
    return ('<li class="d-flex justify-content-between mb-4 user-chat receiver">' +
        '<div class="card mask-custom ">' +
        '<div class="card-body">' +
        '<p class="mb-0">' +
        ' ' + message + '' +
        '</p>' +
        '</div>' +
        '</div>' +
        '</li></br>')
}


function user(id) {
    chatSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/message/'+id
    );
    chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    $(".chat-list").append(senderDiv(data.message))
    };

    chatSocket.onclose = function(e) {
    alert("connection closed");
    };
    $(".chat-list").html('')
    makeAuthAjaxGet('GET', `http://127.0.0.1:8000/user/${id}/`, function(response) {
        if (!response) {
            return
        }
        chatList = $(".chat-list");
        for (i = 0; i < response.length; i++) {
            if (i == 0) {
                $(".chat-list").html('<li id="user">' +
                    '<img src="' + response[0].profile + '" alt="avatar" class="rounded-circle d-flex align-self-start me-3 shadow-1-strong" height="60" width="60">' +
                    '<h4 class="fw-bold mb-0 p-2">' + response[0].name + '</h4>' +
                    '</li>')
            } else if (response[i].sender != true) {
                chatList.append(receiverDiv(response[i].message))
            } else {
                chatList.append(senderDiv(response[i].message))
            }
        }
    })
}