
        
    function likeButtonFormatting(buttonToEdit, isUnlike){
        
        if (isUnlike){
            $(buttonToEdit).css("background-color", "#236807");
            $(buttonToEdit).css("color", "white");
            $(buttonToEdit).css("border-color", "white");
        }
        else{
            alert("change back to green")
            $(buttonToEdit).css("background-color", "red");
            $(buttonToEdit).css("color", "white");
            $(buttonToEdit).css("border-color", "white");

        }
    }

    function like(postOrCommentID, isPost, isUnlike, likes, url, number_of_comments=0){
        // Multiple arguments in url code found at: https://stackoverflow.com/questions/51464131/multiple-parameters-url-pattern-django-2-0
        if (isPost){
            var like_url = url;
            var buttonToEdit = "#like_post";
            var oldLikes = likes;
        }
        else if (postOrCommentID){
            var like_url = url
            var buttonToEdit = "#like_comment_button"
            var oldLikes = likes;
        }
        var xhttp = new XMLHttpRequest();
        xhttp.open("GET", like_url, true);
        xhttp.send();
        alert(isUnlike)
        alert(oldLikes)
        if (isPost){
            xhttp.onreadystatechange = function(){
                if(this.readyState == 4 && this.status == 200){
                var newLikes = JSON.parse(this.responseText);
                newLikes = newLikes.likes.new;
                var textToEdit = "#like_and_comment_info_output";
                var newText = number_of_comments + " comments " + newLikes + " likes";
                $(textToEdit).text(newText);
            }
        };
    }
    else{
        xhttp.onreadystatechange = function(){
            if(this.readyState == 4 && this.status == 200){
                var newLikes = JSON.parse(this.responseText);
                newLikes = newLikes.likes;
                var textToEdit = "#comment_likes";
                var newText = newLikes + " likes";
                $(textToEdit).text(newText);
            }
        };
    }
    likeButtonFormatting(buttonToEdit, isUnlike);
}

    function commentPost(post_id){
        //location.href found at: https://stackoverflow.com/questions/16562577/how-can-i-make-a-button-redirect-my-page-to-another-page
        var redirectURL = "{% url 'thepetproject:create_comment' post.post_id %}";
        location.href= redirectURL;
    }

