document.addEventListener('DOMContentLoaded', () => {
    const prev_content = document.querySelectorAll('.content');
    const edit_area_td = document.querySelectorAll('.edit_area_td');
    const edit_area = document.querySelectorAll('.edit_area');
    const show_textarea = document.querySelectorAll('.edit_btn');
    const edit_btn = document.querySelectorAll('.edit_btn');
    // const post_id = document.querySelector('#post_id');
    

    prev_content.style.display = 'block';
    edit_area_td.style.display = 'none';

    show_textarea.addEventListener('click', () => {
        prev_content.style.display = 'none';
        edit_area_td.style.display = 'block';


        edit_btn.addEventListener('click', () => {
            const post_id = edit_area.dataset.id;
            fetch(`/edit/${post_id}`, {
                method: 'POST',
                body: JSON.stringify({
                    content: edit_area.innerHTML
                })
            }).then(response => response.json())
            .then(response => {
                console.log(response)
            })
        });
    });


});