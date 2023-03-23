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
        }, function(data){
            $('#passwordentry input').val("");
            if (data.success){
                alert("Password Changed!");
            }
            else{
                alert("Could not change password!");
            }
        }, 'json')
    });

    $("#nameentry button").click(function(){
        $.post('',{
            'csrfmiddlewaretoken':csrfmiddlewaretoken,
            'type':'name',
            'name':$('#nameentry input').val()
        }, function(data){
            if (data.success){
                $("#name").text(data.new_name);
                $("#nameentry input").val("")
            }
            else{
                alert("Name change was unsuccessful!");
            }
            
        }, 'json');
    });

    $("#remove_picture").click(function(){
        $.post('',{
            'csrfmiddlewaretoken':csrfmiddlewaretoken,
            'type':'remove'
        }, function(data){
            if (data.success){
                location.reload();
            }
            else{
                alert("Profile picture change unsuccessful!");
            }
        })
    })

    $("#delete-account").click(function(){
        if (window.confirm("Are you sure you want to delete your account? All of your data - posts, profile and comments - will be lost.")){
            $.post("",{
                'csrfmiddlewaretoken': csrfmiddlewaretoken,
                'type':'delete'
            });
        }
    });

});