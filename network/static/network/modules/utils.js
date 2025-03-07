export function EditPost () {

    function getCSRFToken() {
        return document.cookie.split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
    }

    function setEditPost(postId, editContent) {
        fetch(`/editPost/${postId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: JSON.stringify({
                editContent: editContent
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            document.getElementById(`content-${postId}`).textContent = editContent;
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

export function likeDislake() {

    function getCSRFToken() {
        return document.cookie.split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
    }

    function setLikeDislake(postId, reaction) {
        fetch(`/like_dislike/${postId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: JSON.stringify({
                reaction: reaction
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            // Get like or dislike element and change the value and icon
            const likes = data.count['likes'];
            const dislikes = data.count['dislikes'];
            
            const likeElement = document.getElementById(`like-${postId}`);
            const dislikeElement = document.getElementById(`dislike-${postId}`);

            likeElement.innerHTML = `<i class="bi ${reaction === 'like' ? 'bi-hand-thumbs-up-fill' : 'bi-hand-thumbs-up'}"></i>${likes}`;
            dislikeElement.innerHTML = `<i class="bi ${reaction === 'dislike' ? 'bi-hand-thumbs-down-fill' : 'bi-hand-thumbs-down'}"></i>${dislikes}`;
        })
        .catch(error => {
            console.error('Error:', error)
        });
    }
    
    document.querySelectorAll('.reactions').forEach(reaction => {
        reaction.onclick = function(event) {
        event.preventDefault(); // Prevent standart behavior (redirect)

        // Get closest parent div post
        const postDiv = reaction.closest('.post');

        // Get post attr id and find appropriate teg a
        const postId = postDiv.id.split('-')[1];
        console.log(reaction.id)
        
        if (reaction.id === `like-${postId}`) {
            setLikeDislake(postId, 'like'); 
        } else {
            setLikeDislake(postId, 'dislike');
        }
        }
    })
}

