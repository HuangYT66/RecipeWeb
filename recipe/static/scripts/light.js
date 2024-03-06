$(document).ready(function () {
    $("#light").on("change", check_light);
});

function check_light(check) {
    //  get the source element
    var check = true;
    console.log($("#light").val());
    $("#checklight").removeClass();
    $("#checklight").html('<p>loading...</p>');


    let data = {'checkLight': $("#checkLight").val()};
     $.ajax({
        url: "light",
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
                $("#checklight").html('<span style="color: green;">' + server_response + '</span>')
                $("#checklight").addClass("success");
            } else { // failed
                check.val("");
                check.focus();
                $("#checklight").html('<span style="color: red;">' + server_response + '</span>')
                $("#checklight").addClass("failure");
            }
        },
        error: function () {
            $("#checklight").html('<span style="color: red;">Error contacting server</span>');
            $("#checklight").addClass("failure");
        }
    });
}