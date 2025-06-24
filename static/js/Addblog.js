document.getElementById('blogForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const title = document.getElementById('blogTitle').value.trim();
    const content = document.getElementById('editor').innerHTML.trim();
    const tags = document.getElementById('blogTags').value.trim();
    const imageInput = document.getElementById('imageInput');
    let image = '';
    if (imageInput.files && imageInput.files[0]) {
        const reader = new FileReader();
        reader.onload = function(event) {
            image = event.target.result;
            saveBlog({ title, content, tags, image });
        };
        reader.readAsDataURL(imageInput.files[0]);
    } else {
        saveBlog({ title, content, tags, image });
    }
});

function saveBlog(blog) {
    let blogs = JSON.parse(localStorage.getItem('blogs') || '[]');
    const idx = blogs.findIndex(b => b.title === blog.title);
    if (idx !== -1) {
        blogs[idx] = blog; // Update existing blog
    } else {
        blogs.push(blog); // Add new blog
    }
    localStorage.setItem('blogs', JSON.stringify(blogs));
    window.location.href = 'view-blog-list/';
} 