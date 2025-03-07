import { EditPost, likeDislake } from "./modules/utils.js";

document.addEventListener('DOMContentLoaded', () => {
    EditPost();
    likeDislake();
    
    const pageId = document.body.id;

    if (pageId === 'profile-page') {
        import("./modules/profile.js").then(({ initProfile }) => initProfile());
    }
});