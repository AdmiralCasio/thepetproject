

    function delete_post(button, post_id, url, redirect) {
        // Get confirmation incase user clicked it accidentally
        if (confirm("Are you sure you want to delete this post?")) {
            var xhttp = new XMLHttpRequest();
            xhttp.open("GET", url, true);
            xhttp.send();

            xhttp.onreadystatechange = function(){
                if (this.readyState === 4 && this.status === 200) {
                    let response = JSON.parse(this.responseText);
                    // If post was deleted, inform user and redirect them to the home page
                    if (response['success']) {
                        confirm("Post deleted")
                        location.href = redirect;
                    } else {
                        confirm("Error when trying to delete post.")
                    }
                }
            };
        }
    }
        
    function likeButtonFormatting(buttonToEdit, isUnlike){
        
        if (isUnlike){
            $(buttonToEdit).css("background-color", "#236807");
            $(buttonToEdit).css("color", "white");
            $(buttonToEdit).css("border-color", "white");
        }
        else{
            $(buttonToEdit).css("background-color", "red");
            $(buttonToEdit).css("color", "white");
            $(buttonToEdit).css("border-color", "white");

        }
    }

    function like(postOrCommentID, isPost, isUnlike, likes, url, number_of_comments=0){
        // Multiple arguments in url code found at: https://stackoverflow.com/questions/51464131/multiple-parameters-url-pattern-django-2-0
        var newLikes = 0;
        var oldLikes = 0;
        var checkLikes = 0;
        if (isPost){
            var like_url = url;
            var buttonToEdit = "#like_post";
        }
        else if (postOrCommentID){
            var like_url = url
            var buttonToEdit = "#like_comment_button"
        }
        var xhttp = new XMLHttpRequest();
        xhttp.open("GET", like_url, true);
        xhttp.send();
        if (isPost){
            xhttp.onreadystatechange = function(){
                if(this.readyState == 4 && this.status == 200){
                likesJSON = JSON.parse(this.responseText);
                newLikes = likesJSON.likes.new;
                oldLikes = likesJSON.likes.old;
                var textToEdit = "#like_and_comment_info_output";
                var newText = number_of_comments + " comments " + newLikes + " likes";
                $(textToEdit).text(newText);
                checkLikes = oldLikes - 1
                if (newLikes == checkLikes && isUnlike == false){
                    isUnlike = true;
                }
                else if (newLikes != checkLikes && isUnlike == true){
                    isUnlike = false;
                }
                likeButtonFormatting(buttonToEdit, isUnlike);
            }
        };
        }
        else{
            xhttp.onreadystatechange = function(){
                if(this.readyState == 4 && this.status == 200){
                    likesJSON = JSON.parse(this.responseText);
                    newLikes = likesJSON.likes.new;
                    oldLikes = likesJSON.likes.old;
                    var textToEdit = "#comment_likes";
                    var newText = newLikes + " likes";
                    $(textToEdit).text(newText);
                    checkLikes = oldLikes - 1
                    if (newLikes == checkLikes && isUnlike == false){
                        isUnlike = true;
                    }
                    else if (newLikes != checkLikes && isUnlike == true){
                        isUnlike = false;
                    }
                    likeButtonFormatting(buttonToEdit, isUnlike);
                }
            };
        }
        likeButtonFormatting(buttonToEdit, isUnlike);
    }

    function commentPost(post_id, url){
        //location.href found at: https://stackoverflow.com/questions/16562577/how-can-i-make-a-button-redirect-my-page-to-another-page
        var redirectURL = url;
        location.href= redirectURL;
    }

    $(document).ready(function(){
        var darken = $(".darken");
        var info = $("#more_like_info");
        $("#like_and_comment_info_output").click(function(event){
            info.css("visibility", "visible");
            darken.css("filter", "brightness(50%)");
        })

        $(darken).click(function(event){
            if (event.target.id != "like_and_comment_info_output"){
                info.css("visibility", "hidden");
                darken.css("filter", "brightness(100%)");
            }
        })
    })