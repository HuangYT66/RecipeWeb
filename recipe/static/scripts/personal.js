 $(document).ready(function (){
    $("#ShowButton").click(function (event){
        var text = $("#ShowButton").text();
        console.log(text)

        var name = $("#username").text();
        let data = {'username': name};
        console.log(typeof $("#username").text())
        $.ajax({
            url: "showdetails",
            type: "post",
            contentType: "application/json; charset=UTF-8",
            data: JSON.stringify(data),
            success: function (response) {
                var user_gender = response[0]['gender'];
                var user_age= response[1]['age'];
                var user_detail = response[2]['detail'];
                console.log(user_gender);
                console.log(user_age);

                if (text == "Show details"){
                    $("#hiddenInfor").html('<hr class="panel-cover__divider">');
                    $("#hiddenInfor").append('<p className="panel-cover__description">Gender: <a>' + user_gender + '</a></p>');
                    $("#hiddenInfor").append('<hr class="panel-cover__divider">');
                    $("#hiddenInfor").append('<p class="panel-cover__description">Age: <a>' + user_age + '</a></p>');
                    $("#hiddenInfor").append('<hr class="panel-cover__divider">');
                    $("#hiddenInfor").append('<p class="panel-cover__description">Speciality:  <a>' + user_detail + '</a></p>');
                    $("#ShowButton").html('<a id="ShowDetailedInfor" title="Hide details" class="Hide">Hide details</a>')
                }else{
                    $("#hiddenInfor").html('');
                    $("#ShowButton").html('<a id="ShowDetailedInfor" title="Show details" class="Show">Show details</a>')
                }
            },
            error: function () {
            }
        });
    });

});