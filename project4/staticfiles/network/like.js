document.addEventListener('DOMContentLoaded', function(){
    let like_btn = document.querySelector("#like_button");
    let unlike_btn = document.querySelector("#unlike_button");
    
    let like_count = document.querySelector("#like_count");
    
    if (like_btn){
        let post_id = like_btn.dataset.postid;
        like_btn.addEventListener('click', function(event) {
            console.log("Like Button was clicked!");
            fetch(`/like/${post_id}`)
                .then(response => response.json())
                .then((data) => {
                    console.log(data);
                    like_count.innerHTML = data.like_count; 
                    if (data.liked === true){
                        like_btn.style.display = 'none';
                        unlike_btn.style.display = 'block';
                    }
                    else{
                        like_btn.display = "block";
                        unlike_btn.display = "none";
                    }

                });
        });
    }

    if (unlike_btn){
        let post_id = unlike_btn.dataset.postid;
        unlike_btn.addEventListener('click', function(event) {
            console.log("Unlike Button was clicked!");
            fetch(`/unlike/${post_id}`)
                .then(response => response.json())
                .then((data) => {
                    console.log(data);
                    like_count.innerHTML = data.like_count; 
                    if (data.liked === false){
                        like_btn.style.display = 'block';
                        unlike_btn.style.display = 'none';
                    }
                    else{
                        like_btn.display = "none";
                        unlike_btn.display = "block";
                    }

                });
        });
    }
});




