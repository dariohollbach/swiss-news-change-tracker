<script setup></script>

<template>
  <div>
    <h1>News Pages</h1>
    <NewsPage v-for="item in items" :key="item.id" :name="item.title" :id="item.id" />
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
      items: []
    }
  },
  mounted() {
    // Replace with your actual API endpoint
    fetch('http://localhost:1000/api/data/news_papers')
      .then(response => response.json())
      .then(data => {
        this.items = data
      })
      .catch(error => {
        console.error('Error fetching items:', error)
      })
  }
}
</script>

<style>
h1 {
  font-family: Arial, sans-serif;
}
</style>
