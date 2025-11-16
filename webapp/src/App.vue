<script setup></script>

<template>
  <div>
    <h1>News Pages</h1>
    <select v-model="current_news_paper_id">
      <option v-for="item in news_papers" :key="item.id" :value="item.id">
        {{ item.title }}
      </option>
    </select>
    <NewsPage v-if="news_papers.find(np => np.id === current_news_paper_id)" :key="news_papers.find(np => np.id === current_news_paper_id).id" :name="news_papers.find(np => np.id === current_news_paper_id).title" :id="news_papers.find(np => np.id === current_news_paper_id).id" />
  </div>
</template>

<script>
import NewsPage from './components/news_page.vue'

export default {
  name: 'App',
  components: {
    NewsPage
  },
  data() {
    return {
      news_papers: [],
      current_news_paper_id: null
    }
  },
  mounted() {
    // Replace with your actual API endpoint
    fetch('http://localhost:1000/api/data/news_papers')
      .then(response => response.json())
      .then(data => {
        this.news_papers = data
      })
      .catch(error => {
        console.error('Error fetching news_papers:', error)
      })
  }
}


</script>

<style>
h1 {
  font-family: Arial, sans-serif;
}

body {
  font-family: Arial, Helvetica, sans-serif;
}
</style>
