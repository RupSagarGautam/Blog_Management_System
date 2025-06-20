window.addEventListener('DOMContentLoaded', function() {
    const blogListDiv = document.getElementById('blogList');
    renderBlogList();

    function renderBlogList() {
        let blogs = JSON.parse(localStorage.getItem('blogs') || '[]');
        if (blogs.length === 0) {
            blogListDiv.innerHTML = '<p style="text-align:center;color:#888;font-size:1.1rem;">No blog posts created yet.</p>';
            return;
        }
        blogListDiv.innerHTML = blogs.map((blog, idx) => `
            <div class="blog-card">
                <h2>${blog.title}</h2>
                ${blog.image ? `<img src="${blog.image}" alt="Featured Image" class="blog-image" />` : ''}
                <div class="blog-content">${blog.content}</div>
                <div class="blog-tags"><strong>Tags:</strong> ${blog.tags}</div>
                <button class="update-btn" data-idx="${idx}">Update</button>
                <button class="delete-btn" data-idx="${idx}">Delete</button>
            </div>
        `).join('');
        document.querySelectorAll('.delete-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const idx = this.getAttribute('data-idx');
                let blogs = JSON.parse(localStorage.getItem('blogs') || '[]');
                blogs.splice(idx, 1);
                localStorage.setItem('blogs', JSON.stringify(blogs));
                renderBlogList();
            });
        });
        document.querySelectorAll('.update-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const idx = this.getAttribute('data-idx');
                window.location.href = `UpdateBlog.html?idx=${idx}`;
            });
        });
    }
}); 