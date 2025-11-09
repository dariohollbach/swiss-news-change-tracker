
fetch('http://localhost:1000/api/data/news_papers')
    .then(response => response.json())
    .then(data => {
        for (const paper of data) {
            const paperElement = document.createElement('h2');
            paperElement.textContent = paper.title;
            const paperArticlesContainer = document.createElement('ul');
            paperArticlesContainer.id = `articles-for-paper-${paper.id}`;
            paperElement.appendChild(paperArticlesContainer);
            fetch(`http://localhost:1000/api/data/news_papers/${paper.id}/articles`)
                .then(response => response.json())
                .then(articles => {
                    for (const article of articles) {
                        const articleElement = document.createElement('li');
                        articleElement.textContent = article.title; 
                        document.getElementById(`articles-for-paper-${paper.id}`).appendChild(articleElement);
                    }
                })
                .catch(error => {
                    console.error('Error fetching news papers:', error);
                });
            document.getElementById('news-papers').appendChild(paperElement);
        }
    })
    .catch(error => {
        console.error('Error fetching news papers:', error);
    });