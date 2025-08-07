window.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const searchButton = document.getElementById('searchButton');
    const blogListDiv = document.getElementById('blogList');
    let blogCards = Array.from(blogListDiv.getElementsByClassName('blog-card'));

    // Retrieve deleted blog IDs from localStorage
    let deletedBlogIds = JSON.parse(localStorage.getItem('deletedBlogIds') || '[]');

    // Remove blogs from UI that are in deletedBlogIds
    blogCards.forEach(card => {
        const blogId = card.getAttribute('data-id');
        if (deletedBlogIds.includes(blogId)) {
            card.remove();
        }
    });

    function filterBlogs() {
        const query = searchInput.value.toLowerCase();
        blogCards.forEach(card => {
            const title = card.getAttribute('data-title');
            const author = card.getAttribute('data-author');
            const created = card.getAttribute('data-created');
            if (title.includes(query) || author.includes(query) || created.includes(query)) {
                card.style.display = '';
            } else {
                card.style.display = 'none';
            }
        });
    }

    searchInput.addEventListener('input', filterBlogs);
    searchButton.addEventListener('click', filterBlogs);

    window.deleteBlog = function(button) {
        console.log('deleteBlog called');
        const blogCard = button.closest('.blog-card');
        if (blogCard) {
            const blogId = blogCard.getAttribute('data-id');
            // Add blogId to deletedBlogIds and save to localStorage
            if (!deletedBlogIds.includes(blogId)) {
                deletedBlogIds.push(blogId);
                localStorage.setItem('deletedBlogIds', JSON.stringify(deletedBlogIds));
            }
            blogCard.remove();
            // Update blogCards array after removal
            blogCards = Array.from(blogListDiv.getElementsByClassName('blog-card'));
        }
    };
});
