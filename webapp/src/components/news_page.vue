<template>
  <div>
    <h2>{{ id }} | {{ name }}</h2>
    <ul>
      <Article v-for="item in articles" :key="item.id" :name="item.title" :id="item.id" :content="item.content" />
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
      articles: []
    }
  },
  mounted() {
    fetch(`http://localhost:1000/api/data/news_papers/${this.id}/articles`)
      .then(response => response.json())
      .then(data => {
        this.articles = data
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
