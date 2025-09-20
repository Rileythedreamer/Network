document.addEventListener('DOMContentLoaded', () => {
    
    const show_textarea_links = document.querySelectorAll('.show_textarea');
    
    const contents = document.querySelectorAll('.content');
    contents.forEach(content => {
        content.querySelector('.edit-area').style.display = 'none';
        content.querySelector('.prev-content').style.display = 'block';
    });
    
    

    show_textarea_links.forEach(function (edit_link) {
        edit_link.addEventListener('click', function() {

            
            
            const prev_content = this.parentNode;
            const edit_area = this.parentNode.parentNode.querySelector('.edit-area');

            // Display edit area
            prev_content.style.display = 'none';
            edit_area.style.display = 'block';

            // after they wanna save edits

            const edit_btn = edit_area.querySelector('.edit_btn');
            edit_btn.addEventListener('click', function () {
                const post_id = this.dataset.id;
                const content_td = this.parentNode.parentNode;
                console.log(this.dataset.id)
                fetch(`/edit/${post_id}`, {
                    method: 'POST',
                    headers: {'X-CSRFToken': csrftoken},
                    body: JSON.stringify({
                        content: edit_area.value()
                    })
                }).then(response => response.json())
                .then(response => {
                    console.log(response)
                    
                    
                    
                })

                fetch(`/get_new_content/${post_id}`)
                .then(response => response.json())
                .then(new_content => {
                    console.log(new_content);
                    content_td.querySelector('.prev-content').innerHTML = new_content;
                })
                content_td.querySelector('.prev-content').style.display = 'block';
                content_td.querySelector('.edit-area').style.display = 'none';
                
        });


        });
    });

});

