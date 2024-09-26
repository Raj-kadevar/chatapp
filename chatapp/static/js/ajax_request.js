function makeAuthAjaxGet(methodType, url, callback) {
    const headers = {'Authorization': 'Token ' + localStorage.getItem("access_token")};
    $.ajax({
        method: methodType,
        headers: headers,
        url: url,
        contentType: false,
        success: function (data) {
            if (callback) {
                callback(data)
            }
        },

    });
}

function makeAuthAjaxRequest(methodType, csrfToken, url, data, callback)
{
    const headers = {'X-CSRFToken': csrfToken};
    $.ajax({
        method: methodType,
        headers: headers,
        url: url,
        data: data,
        success: function (data) {
            if (callback) {
                callback(data)
            }
        },
        error: function (data) {
             if (callback) {
                callback(data)
            }
        },

    });
}

function makeAjaxPost(url, data, callback) {
    const headers = {'Authorization': 'Token ' + localStorage.getItem("access_token")};
    $.ajax({
        type: 'POST',
        headers: headers,
        url: url,
        data: data,
        processData: false,
        contentType: false,
        success: function (data) {
            if (callback) {
                callback(data)
            }
        },
        error: function (data) {
             if (callback) {
                callback(data)
            }
        },

    });
}

function makeFileAjaxPost(type, url, data, callback) {
    const headers = {'Authorization': 'Token ' + localStorage.getItem("access_token")};
    $.ajax({
             url:url,
             type: type,
             headers: headers,
             data: data,
             success: function (data) {
                if (callback) {
                    callback(data)
                }
             },
             error: function (data) {
                 if (callback) {
                    callback(data)
                 }
             },
            cache: false,
            contentType: false,
            processData: false
    });
}


