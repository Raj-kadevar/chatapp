$("#submit").click(function(event){
    $(this).attr("disabled", true);
    $('span').text('')
    event.preventDefault();
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    var formdata = $("#login_form").serialize();
    makeAuthAjaxRequest('POST', csrfToken, "http://127.0.0.1:8000/login/api/", formdata, function(response) {
        if (response.responseText) {
           $('#error').text("Please enter valid credentials");
           $('.button').html('&times;');
           $("#submit").attr("disabled", false);
        }
        else {
           $(this).attr("disabled", true);
           $('.alert-dismissible').hide();
           localStorage.setItem("access_token",response.token);
           window.location.href = "http://127.0.0.1:8000/index/"
        }
    })

});