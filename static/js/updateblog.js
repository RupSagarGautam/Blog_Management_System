function getQueryParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

document.addEventListener('DOMContentLoaded', function() {
    const idx = getQueryParam('idx');
    if (idx !== null) {
        let blogs = JSON.parse(localStorage.getItem('blogs') || '[]');
        const blog = blogs[parseInt(idx)];
        if (blog) {
            document.getElementById('blogTitle').value = blog.title;
            document.getElementById('blogContent').value = blog.content;
            document.getElementById('blogTags').value = blog.tags;
            if (blog.image) {
                const imagePreview = document.getElementById('imagePreview');
                imagePreview.innerHTML = `<img src="${blog.image}" alt="Featured Image" style="max-width: 200px; max-height: 200px; border-radius: 8px;" />`;
            }
        }
    }
});

document.getElementById('updateBlogForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const title = document.getElementById('blogTitle').value.trim();
    const content = document.getElementById('blogContent').value.trim();
    const tags = document.getElementById('blogTags').value.trim();
    const imageInput = document.getElementById('imageInput');
    let image = '';
    if (imageInput.files && imageInput.files[0]) {
        const reader = new FileReader();
        reader.onload = function(event) {
            image = event.target.result;
            updateBlog({ title, content, tags, image });
        };
        reader.readAsDataURL(imageInput.files[0]);
    } else {
        // Try to keep the old image if not updated
        let blogs = JSON.parse(localStorage.getItem('blogs') || '[]');
        const idx = blogs.findIndex(b => b.title === title);
        if (idx !== -1) {
            image = blogs[idx].image || '';
        }
        updateBlog({ title, content, tags, image });
    }
});

function updateBlog(updatedBlog) {
    let blogs = JSON.parse(localStorage.getItem('blogs') || '[]');
    const idx = blogs.findIndex(b => b.title === updatedBlog.title);
    if (idx !== -1) {
        blogs[idx] = updatedBlog;
        localStorage.setItem('blogs', JSON.stringify(blogs));
        window.location.href = 'view-blog-list/';
    } else {
        alert('No blog found with this title to update.');
    }
}
