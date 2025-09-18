document.addEventListener('DOMContentLoaded', () => {
    const contents = document.querySelectorAll('.content');
    
    contents.forEach(content => {
        content.closest('.edit-area-td').style.display = 'none';
        content.closest('.prev-content').style.display = 'block';
    });
    show_textarea_links = document.querySelectorAll('.show_textarea');

    show_textarea_links.forEach(edit_link => {
        edit_link.addEventListener('click', () => {
            const this_post_row = this.parentNode.parentNode;
            const content_td = this.parentNode;
            const edit_area_td = this_post_row.closest('.edit_area_td');

            // Display edit area
            content_td.style.display = 'none';
            edit_area_td.style.display = 'block';


        });
    });

    
    


});