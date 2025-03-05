export function EditPost () {

    function setEditPost(postId, editContent) {
        fetch(`/editPost/${postId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                editContent: editContent
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            document.getElementById(`content-${postId}`).innerHTML = editContent
        })
        .catch(error => {
            console.error('Error:', error);
        });

    }

    const editLinks = document.querySelectorAll('.edit-link');

    editLinks.forEach(link => {
        link.onclick = function(event) {
            event.preventDefault(); // Prevent redirect link
            
            // Get parent div with class post 
            const postDiv = link.closest('.post');

            // Find appropriate div with class edit-post
            const postId = postDiv.id.split('-')[1];
            const editDiv = document.getElementById(`edit-post-${postId}`);

            // Change display in div
            postDiv.style.display = 'none';
            editDiv.style.display = 'block';

            // Add event to the edit-form
            document.getElementById(`edit-form-${postId}`).onsubmit = function(event) {
                event.preventDefault(); // Prevent standart behavior submit form
                // Get edit content
                const editContent = document.getElementById(`edit-content-${postId}`).value;

                setEditPost(postId, editContent);
                // Update content
                postDiv.style.display = 'block';
                editDiv.style.display = 'none';
            }
        }
    });

}