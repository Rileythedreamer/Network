document.addEventListener('DOMContentLoaded', () => {
    
    const show_textarea_links = document.querySelectorAll('.show_textarea');
    
    const contents = document.querySelectorAll('.table-data-content');
    contents.forEach(content => {
        content.querySelector('.edit-area').style.display = 'none';
        content.querySelector('.content-area').style.display = 'block';
    });
    
    

    show_textarea_links.forEach(function (edit_link) {
        edit_link.addEventListener('click', function() {
            const prev_content = this.closest('.content-area');
            const edit_area = this.closest('.table-data-content').querySelector('.edit-area');
            
            // Display edit area
            prev_content.style.display = 'none';
            edit_area.style.display = 'block';

            // after they wanna save edits

            const save_edits = edit_area.querySelector('.save_edits');
            save_edits.addEventListener('click', function () {
                
                
                const post_id = this.dataset.id;
                const edit_area = this.closest('.edit-area');
                const content_area = this.closest('.table-data-content').querySelector('.content-area');
                const new_content = this.parentNode.querySelector('.new-content');
                UpdateandGetdata();
                async function UpdateandGetdata(){
                    // send the data to the server
                await fetch(`/edit/${post_id}`, {
                    method: 'POST',
                    headers: {'X-CSRFToken': csrftoken},
                    body: JSON.stringify({
                        content: new_content.value
                    })
                }).then(response => response.json())
                .then(response => {
                    // console.log(response)
                })


                //  update post content with new data
                
                
                    fetch(`/get_new_content/${post_id}`)
                    .then(response => response.json())
                    .then(data => {
                        content_area.querySelector('.content').innerText = data.content;
                    })
                    edit_area.style.display = 'none';
                    content_area.style.display = 'block';
                }
        });


        });
    });

});

