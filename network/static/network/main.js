import { initProfile } from "./modules/profile.js";

document.addEventListener('DOMContentLoaded', () => {
    const pageId = document.body.id;

    if (pageId === 'profile-page') {
        initProfile();
    }
});