$(document).ready(function(){
    $("#sidebar-icon").click(function(){
        console.log("Clicked");
        $(".sidebar").slideToggle("slow");
    });
});