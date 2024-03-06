//real_time refresh
$(document).ready(function () {
    $("#username").on("change", check_username);
});

function check_username() {
    //  get the source element
    var chosen_user = $(this).find("input");
    console.log($("#username").val());
    $("#checkuser").removeClass();
    $("#checkuser").html('<p>loading...</p>');

    // ajax code
    // $.post('/checkuser', {
    //     'username': chosen_user.val()
    // }).done(function (response) {
    //     var server_response = response['text']
    //     var server_code = response['returnvalue']
    //     if (server_code == 0) { // success
    //         $("#input_password").focus();
    //         $("#checkuser").html('<span>' + server_response + '</span>')
    //         $("#checkuser").addClass("success");
    //     } else { // failed
    //         chosen_user.val("");
    //         chosen_user.focus();
    //         $("#checkuser").html('<span>' + server_response + '</span>')
    //         $("#checkuser").addClass("failure");
    //     }
    // }).fail(function () {
    //     $("#checkuser").html('<span>Error contacting server</span>');
    //     $("#checkuser").addClass("failure");
    // })
    let data = {'username': $("#username").val()};
    $.ajax({
        url: "checkuser",
        type: "post",
        contentType: "application/json; charset=UTF-8",
        data: JSON.stringify(data),
        success: function (response) {
            var server_response = response[0]['text'];
            var server_code = response[1]['returnvalue'];
            console.log(response);
            console.log(server_code);

            if (server_code == 0) { // success
                $("#input_password").focus();
                $("#checkuser").html('<span style="color: green;">' + server_response + '</span>')
                $("#checkuser").addClass("success");
            } else { // failed
                chosen_user.val("");
                chosen_user.focus();
                $("#checkuser").html('<span style="color: red;">' + server_response + '</span>')
                $("#checkuser").addClass("failure");
            }
        },
        error: function () {
            $("#checkuser").html('<span style="color: red;">Error contacting server</span>');
            $("#checkuser").addClass("failure");
        }
    });
}