export function initProfile() {
    
    function setFollowValues(action, userId) {
        fetch(`/follow/${userId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                action: action
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data)

            if (action === 'follow') {
                document.getElementById('follow-btn').style.display = 'none';
                document.getElementById('unfollow-btn').style.display = 'block';
            } else {
                document.getElementById('follow-btn').style.display = 'block';
                document.getElementById('unfollow-btn').style.display = 'none';
            }
            document.getElementById('followers').innerHTML = `${data.followers} followers`
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
    }



    document.getElementById('follow-btn').onclick = function() {
        const userId = this.dataset.user;
        setFollowValues('follow', userId);
    };
    document.getElementById('unfollow-btn').onclick = function() {
        const userId = this.dataset.user;
        setFollowValues('unfollow', userId);
    };
}