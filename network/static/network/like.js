document.addEventListener('DOMContentLoaded', function() {
    const like_btns = document.querySelectorAll('.like_btn');

    like_btns.forEach(function(like_btn){
        like_btn.addEventListener('click', function() {
            const post_id = this.dataset.id
            const no_of_likes = this.parentNode.querySelector('.no_of_likes');
            var lik = this.dataset.like
            if (lik === "true"){
                lik = true
            }else if (lik==="false"){
                lik = false
            }
                
            fetch(`/like/${post_id}`, {
                method: 'PUT',
                headers: {'X-CSRFToken': csrftoken},
                body: JSON.stringify({
                    liked: lik
                })
            })
            .then(response => response.json())
            .then(response =>{
                no_of_likes.innerText = response.likes
            })
            .catch(error => console.log(error))
            this_btn = document.querySelector(`[data-id="${post_id}"][data-like="${lik}"]`);
            opp_btn = document.querySelector(`[data-id="${post_id}"][data-like="${!lik}"]`);
            
            
            console.log(lik)
            this_btn.style.display = 'none';
            opp_btn.style.display = 'block';
        });
    });
})


