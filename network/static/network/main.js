import { EditPost, likeDislake, AddPostMessage } from "./modules/utils.js";

document.addEventListener('DOMContentLoaded', () => {
    EditPost();
    likeDislake();
    AddPostMessage();
    
    const pageId = document.body.id;

    if (pageId === 'profile-page') {
        import("./modules/profile.js").then(({ initProfile }) => initProfile());
    }
});