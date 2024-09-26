StatusSocket = new WebSocket('ws://' + window.location.host + '/ws/status/');
function submit(e) {
            event.preventDefault();
            if (allFiles.length >= 1) {
                var formdata = new FormData();
                for (var i = 0; i < allFiles.length; i++) {
                    formdata.append('files', allFiles[i]);
                }
                ;
                formdata.append('sender', parseInt($("#user").text()))
                formdata.append('receiver', receiver)
                makeFileAjaxPost('POST', 'http://127.0.0.1:8000/api/files/', formdata, function(response) {
                        if (response.document_len) {
                            chatSocket.send(JSON.stringify({
                                'document_len': response.document_len,
                                'user': parseInt($("#user").text())
                            }));
                        }else{
                            alert("error in file");
                        }
                });

            } else {
                message = $('#txtArea').val();
                if ($('#txtArea').val().trim() != '') {

                    chatSocket.send(JSON.stringify({
                        'message': message.replace(/(<([^>]+)>)/ig, ''),
                        'user': parseInt($("#user").text())
                    }));
                }
            }
            $('#txtArea').val('');
            $('.preview').text('');
            allFiles = []
            $(".chat-list").animate({
                scrollTop: $(
                    '.chat-list').get(0).scrollHeight
            }, 1000);
        }

function senderImgDiv(file) {

    return ('<div><li class="d-flex justify-content-between mb-4 user-chat sender">' +
        '<div class="card mask-custom ">' +
        '<div class="card-body">' +
        '<img class="mb-0" src='+file+' height="140px" width="98px">' +
        '</p>' +
        '</div>' +
        '</div>' +
        '</li></div>')
}

function receiverImgDiv(file) {

    return ('<div><li class="d-flex justify-content-between mb-4 user-chat receiver">' +
        '<div class="card mask-custom ">' +
        '<div class="card-body">' +
        '<img class="mb-0" src='+file+' height="140px" width="98px">' +
        '</p>' +
        '</div>' +
        '</div>' +
        '</li></div>')
}


function senderDiv(message) {
    return ('<div><li class="d-flex justify-content-between mb-4 user-chat sender">' +
        '<div class="card mask-custom ">' +
        '<div class="card-body">' +
        '<p class="mb-0">' +
        ' ' + message + '' +
        '</p>' +
        '</div>' +
        '</div>' +
        '</li></div>')
}

function receiverDiv(message) {
    return ('<div><li class="d-flex justify-content-between mb-4 user-chat receiver">' +
        '<div class="card mask-custom ">' +
        '<div class="card-body">' +
        '<p class="mb-0">' +
        ' ' + message + '' +
        '</p>' +
        '</div>' +
        '</div>' +
        '</li></div>')
}

var checkConnection = false
var url = 0
var receiver = 0
function user(id) {
    receiver = id
    if(url != 0){
        if('ws://' + window.location.host + '/ws/message/'+id != url){
            chatSocket.close()
            checkConnection = false
        }else{
            checkConnection = true
        }
    }
    if(checkConnection == false){
        chatSocket = new WebSocket(
        'ws://' + window.location.host + '/ws/message/'+id);
        url = 'ws://' + window.location.host + '/ws/message/'+id
        checkConnection = true
    }
    chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    let myAudio = document.querySelector('#audio')
            if(data.files){
                for(i=0; i<data.files.length; i++){
                    if(data.sender == true){
                        $(".chat-list").append(senderImgDiv(data.files[i]))
                    }else{
                        $(".chat-list").append(receiverImgDiv(data.files[i]))
                        myAudio.play()
                    }
                }
            }else{
                if(data.sender == true){
                    $(".chat-list").append(senderDiv(data.message))
                }else{
                    $(".chat-list").append(receiverDiv(data.message))
                    myAudio.play()
                }
            }
     $(".chat-list").animate({
                    scrollTop: $(
                      '.chat-list').get(0).scrollHeight
                }, 1000);
    };

    $(".chat-list").html('')
    makeAuthAjaxGet('GET', `http://127.0.0.1:8000/user/${id}/`, function(response) {
        if (!response) {
           window.location.href = "http://127.0.0.1:8000/login/"
        }
        chatList = $(".chat-list");
        $(".chat-list").html('<li id="user" class="sticky-top">' +
                    '<img src="' + response.profile[0].profile + '" alt="avatar" class="rounded-circle d-flex align-self-start me-3 shadow-1-strong" height="60" width="60">' +
                    '<h4 style="float:left;" class="fw-bold mb-0 p-2">' + response.profile[0].name + '</h4>' +
                    '</li>')
        for (i = 0; i < response.messages.length; i++) {
            if(response.messages[i].message != null){
                if (response.messages[i].sender == id) {
                    chatList.append(receiverDiv(response.messages[i].message))
                } else {
                    chatList.append(senderDiv(response.messages[i].message))
                }
            }else{
                if(response.messages[i].sender != id){
                    chatList.append(senderImgDiv(response.messages[i].images))
                }else{
                    chatList.append(receiverImgDiv(response.messages[i].images))
                }
            }
        }
        $(".chat-list").animate({
                    scrollTop: $(
                      '.chat-list').get(0).scrollHeight
        }, 1500);
    })
}
var status = $(this).prop('checked');
$('#status').change(function () {
    status = $(this).prop('checked');
    makeAuthAjaxGet('GET', 'http://127.0.0.1:8000/api/user/status/?status='+status, function(response) {
        return
    });
})

StatusSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        if(data.status == true){
            $("#"+data.id).html("<i class='fas fa-smile' style='font-size:28px;color:green'></i>")
        }else{
            $("#"+data.id).html("<i class='far fa-frown' style='font-size:28px;'></i>")

        }
};

StatusSocket.close = function(){
    alert("status closed");
}

   function dragOverHandler(ev) {
        ev.preventDefault();
        console.log("dragOver");
    }

var allFiles = []

$("#txtArea").on('drop', function (e) {
    e.preventDefault();
    const files = e.originalEvent.dataTransfer.files;
    for(i=0 ; i<files.length ; i++)
    {
        allFiles[i] = files[i]
    }
    showPreview();
});

function showPreview() {
  for (let i = 0; i < allFiles.length; i++) {
    src = URL.createObjectURL(allFiles[i])
    ;


      $(".preview").append('<div class="side_view" id=' + i + '>' +
        '<button class="btn btn-outline-danger" onclick="removeImage(' + i + ')"><i class="fa fa-times" aria-hidden="true"></i></button>' +
        '<img src=' + src + ' height="40%" width="10%"> </div>');
  }
}

function removeImage(index){
    allFiles.splice(index,1);
    $(".preview").html('')
    showPreview()
}

$('#audios').change(function(e){
    $("#audio").attr("src","http://127.0.0.1:8000/media/audio/"+$("#audios").val());
    makeAuthAjaxGet('GET', 'http://127.0.0.1:8000/api/tune/?audio='+$("#audios").val(), function(response){
        if (response.status) {
           alert("tune changed successfully");
        }
    });
})