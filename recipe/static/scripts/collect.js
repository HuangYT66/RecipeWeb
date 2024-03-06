$(document).ready(function (){
    $("#collectButton").click(function (event){
        var text = $("#collectButton").text();
        console.log(text)

        var dishname = $("h2").text();
        console.log(dishname)

        if(text == "collect"){
            let data = {'dishname': dishname};
            $.ajax({
                url: "/addcollection",
                type: "post",
                contentType: "application/json; charset=UTF-8",
                data: JSON.stringify(data),
                success: function (response) {
                    // var content = response[0]['cancel'];
                    var user = response[1]['username'];
                    console.log(user)
                    if (user === null){
                        alert("Please login first!")
                    }else{
                        $("#collectButton").text("cancel")
                    }

                    // $("#collectButton").innerHTML = '<img src="../static/img/rec_oper_save.png" alt="">cancel'
                },
                error: function () {
                }
            });
        }else{
            let data = {'dishname': dishname};
            $.ajax({
                url: "/deletecollection",
                type: "post",
                contentType: "application/json; charset=UTF-8",
                data: JSON.stringify(data),
                success: function (response) {
                    // var content = response[0]['cancel'];
                    $("#collectButton").text("collect")
                    // $("#collectButton").innerHTML = '<img src="../static/img/rec_oper_save.png" alt="">cancel'
                },
                error: function () {
                }
            });
        }

    });

});