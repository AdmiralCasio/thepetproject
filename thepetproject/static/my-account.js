$(document).ready(function(){   
    $("#changename").click(function(){
        $("#nameentry").css("display", "inline");
    });
    
    $("#changepassword").click(function(){
        $("#passwordentry").css("display", "inline");
    });

    $("#changepicture").click(function(){
        $("#pictureentry").css("display", "inline");
    });
    $("#passwordentry button").click(function(){
        $.post('',{
            'csrfmiddlewaretoken':csrfmiddlewaretoken,
            'type':'password',
            'password':$('#passwordentry input').val()
        }).done(function(){
            $('#passwordentry input').val("");
        })
    });

    $("#nameentry button").click(function(){
        $.post('',{
            'csrfmiddlewaretoken':csrfmiddlewaretoken,
            'type':'name',
            'name':$('#nameentry input').val()
        }, function(data){
            location.reload();
        });
    });

    $("#delete-account").click(function(){
        if (window.confirm("Are you sure you want to delete your account? All of your data - posts, profile and comments - will be lost.")){
            $.post("",{
                'csrfmiddlewaretoken': csrfmiddlewaretoken,
                'type':'delete'
            });
        }
    });

});