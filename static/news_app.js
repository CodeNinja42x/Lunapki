// Apply filter based on category selection
function applyFilter() {
    const selectedFilter = document.getElementById('news-filter').value;
    fetchNews(selectedFilter);
}

// Fetch news based on the selected category
function fetchNews(category = 'general') {
    const apiUrl = `/api/news?category=${category}`;
    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            updateNewsContainer(data.articles);
        })
        .catch(error => console.error('Error fetching news:', error));
}

// Update the news container with fetched news
function updateNewsContainer(articles) {
    const newsContainer = document.getElementById('news-container');
    newsContainer.innerHTML = ''; // Clear previous news

    if (articles.length === 0) {
        newsContainer.innerHTML = '<p>No news available.</p>';
        return;
    }

    articles.forEach(article => {
        const articleHtml = `
            <div class="news-item">
                <h3>${article.flash_alert.headline}</h3>
                <p>${article.description || 'Description not available'}</p>
                <p><strong>Sentiment:</strong> ${article.flash_alert.sentiment.label} (Score: ${article.flash_alert.sentiment.score})</p>
                <p><strong>Keywords:</strong> ${article.flash_alert.keywords.join(', ')}</p>
                <div class="sentiment-bar" style="width: ${article.flash_alert.sentiment.score * 100}%; background-color: ${article.flash_alert.sentiment.label === 'Positive' ? 'green' : 'red'}"></div>
                
                <!-- Comment Form -->
                <form class="comment-form">
                    <input type="text" id="user-name-${article.title}" placeholder="Your name" required>
                    <textarea id="comment-${article.title}" placeholder="Your comment" required></textarea>
                    <button type="submit" onclick="submitComment('${article.title}')">Submit Comment</button>
                </form>

                <!-- Social Sharing -->
                <div class="share-buttons">
                    <a href="https://twitter.com/intent/tweet?text=Check%20this%20out!%20${article.url}">Share on Twitter</a>
                    <a href="https://www.linkedin.com/shareArticle?mini=true&url=${article.url}">Share on LinkedIn</a>
                </div>
            </div>
        `;

        newsContainer.innerHTML += articleHtml;
    });
}

// Submit comment
function submitComment(articleId) {
    const userName = document.getElementById(`user-name-${articleId}`).value;
    const comment = document.getElementById(`comment-${articleId}`).value;

    fetch('/submit_comment', {
        method: 'POST',
        body: JSON.stringify({ article_id: articleId, user_name: userName, comment: comment }),
        headers: { 'Content-Type': 'application/json' }
    }).then(response => response.json()).then(data => {
        if (data.status === 'success') {
            alert('Comment submitted successfully!');
        }
    }).catch(error => console.error('Error submitting comment:', error));
}

// Onload, fetch general news
document.addEventListener('DOMContentLoaded', () => {
    fetchNews();
});
