<template>
  <div>
    <div class="acticles-control">
      <div id="date-sort-control">
        <div class="date-filters">
          <label for="start-date">From:</label>
          <input type="date" id="start-date" v-model="startDate">
          <label for="end-date">To:</label>
          <input type="date" id="end-date" v-model="endDate">
        </div>
        <button @click="toggleSort" id="date-sort-button">
          <span v-if="sortAscending">Sort Desc</span>
          <span v-else>Sort Asc</span>
        </button>
      </div>

      <button @click="only_show_differences = !only_show_differences" :class="{ 'on-state': only_show_differences }"
        id="show-differences-button">
        <span v-if="only_show_differences">Show All</span>
        <span v-else>Only Show Differences</span>
      </button>

      <span></span>
      <span>Anzahl Artikel: {{ articles.length }}</span>
      <span>Publication Date</span>
      <span>Änderungen {{articles.reduce((total, article) => total + article.changes.length, 0)}}</span>
    </div>
    <ul>
      <template v-for="article in sortedArticles" :key="article.id">
        <Article v-if="article.changes.length > 0 || !only_show_differences" :name="article.title" :id="article.id"
          :content="article.content" :changes="article.changes" :publication_date="article.publication_date"
          @article-deleted="handleArticleDeleted" />
      </template>
    </ul>
  </div>
</template>

<script>
import Article from './article.vue';

export default {
  name: 'NewsPage',
  components: {
    Article
  },
  props: {
    name: {
      type: String,
      required: true
    },
    id: {
      type: [String, Number],
      required: true
    }
  },
  data() {
    return {
      articles: [],
      only_show_differences: false,
      sortAscending: false, // false for descending (newest first), true for ascending (oldest first)
      startDate: '2025-11-10',
      endDate: '2025-11-20'
    }
  },
  computed: {
    sortedArticles() {
      return [...this.articles].sort((a, b) => {
        const dateA = new Date(a.publication_date);
        const dateB = new Date(b.publication_date);
        if (this.sortAscending) {
          return dateA - dateB; // Ascending
        }
        return dateB - dateA; // Descending
      });


    }
  },
  watch: {
    startDate() {
      this.fetchArticles();
    },
    endDate() {
      this.fetchArticles();
    }
  },
  mounted() {
    this.fetchArticles();
  },
  methods: {
    fetchArticles() {
      let url = `http://localhost:1000/api/data/news_papers/${this.id}/articles?`;
      if (this.startDate) url += `start_date=${this.startDate}&`;
      if (this.endDate) url += `end_date=${this.endDate}&`;
      fetch(url).then(response => response.json())
        .then(data => {
          this.articles = data
          for (const article of this.articles) {
            fetch(`http://localhost:1000/api/data/articles/${article.id}/changes`)
              .then(response => response.json())
              .then(data => {
                article.changes = data;
              })
              .catch(error => {
                console.error('Error fetching article changes:', error);
              });
          }
        })
        .catch(error => {
          console.error('Error fetching articles:', error)
        })
    },
    toggleSort() {
      this.sortAscending = !this.sortAscending;
    },
    handleArticleDeleted(articleId) {
      this.articles = this.articles.filter(article => article.id !== articleId);
    }
  }
}
</script>

<style scoped>
p {
  font-size: 16px;
  margin: 4px 0;
}

ul {
  padding: 0;
}

.acticles-control {
  gap: 10px;
  display: grid;
  grid-template-columns: 12fr 4fr 3fr 1fr;
  align-items: end;
  margin-bottom: 10px;
  padding: 8px;
}

.date-filters {
  grid-column: 1;
  display: flex;
  align-items: start;
  flex-direction: column;
  gap: 5px;
}

.date-filters label {
  font-size: 14px;
}

#show-differences-button {
  grid-column: 3;
}

#show-differences-button,
#date-sort-button {
  padding: 8px;
  font-size: 14px;
  cursor: pointer;
  border: 1px solid #ccc;
  border-radius: 4px;
  background-color: #f9f9f9;
  white-space: nowrap;
  width: 100%;
}

.date-filters input[type="date"] {
  padding: 6px;
}

#date-sort-control {
  grid-column: 2;
  gap: 5px;
  justify-items: stretch;
  display: flex;
  align-items: start;
  flex-direction: column;
}
</style>
