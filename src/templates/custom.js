window.addEventListener('DOMContentLoaded', (e) => {
    document.getElementById('recent-list').innerHTML = `
    {% for gallery in recent %}
    <li><a href="{{gallery.link}}">{{gallery.title}}</a></li>
    {% endfor %}
    `;
});