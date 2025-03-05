import { EditPost } from "./modules/utils.js";

document.addEventListener('DOMContentLoaded', () => {
    EditPost();
    
    const pageId = document.body.id;

    if (pageId === 'profile-page') {
        import("./modules/profile.js").then(({ initProfile }) => initProfile());
    }
});