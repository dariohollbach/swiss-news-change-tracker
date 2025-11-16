<template>
  <div>
    <h2>{{ id }} | {{ name }}</h2>
    <ul>
      <button @click="only_show_differences = !only_show_differences" :class="{ 'on-state': only_show_differences }">
        <span v-if="only_show_differences">Show All</span>
        <span v-else>Only Show Differences</span>
      </button>
      <template v-for="article in articles" :key="article.id">
        <Article v-if="article.changes.length > 0 || !only_show_differences" :name="article.title" :id="article.id"
          :content="article.content" :changes="article.changes" :publication_date="article.publication_date" />
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
      only_show_differences: false
    }
  },
  mounted() {
    fetch(`http://localhost:1000/api/data/news_papers/${this.id}/articles`)
      .then(response => response.json())
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
</style>
