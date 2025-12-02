<script setup></script>

<template>
  <div>
    <header>
      <h1>Swiss News Change Tracker</h1>
    </header>
    <main>
      <select v-model="current_news_paper_id" id="select-news-paper">
        <option v-for="item in news_papers" :key="item.id" :value="item.id">
          {{ item.title }}
        </option>
      </select>
      <NewsPage v-if="news_papers.find(np => np.id === current_news_paper_id)"
        :key="news_papers.find(np => np.id === current_news_paper_id).id"
        :name="news_papers.find(np => np.id === current_news_paper_id).title"
        :id="news_papers.find(np => np.id === current_news_paper_id).id" />
    </main>
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
    fetch('http://localhost:1000/api/data/news_papers')
      .then(response => response.json())
      .then(data => {
        this.news_papers = data
        if (this.news_papers.length > 0) {
          this.current_news_paper_id = this.news_papers[0].id;
        }
      })
      .catch(error => {
        console.error('Error fetching news_papers:', error)
      })
  }
}


</script>

<style>
header {
  text-align: center;
  width: 100%;
  background-color: rgb(181, 243, 222);
  padding: 20px 0;
  margin-bottom: 20px;
}

h1 {
  margin: 0;
  font-family: Arial, Helvetica, sans-serif;
}

body {
  margin: 0;
  font-family: Arial, Helvetica, sans-serif;
}

main {
  margin: 0 10%;
}

#select-news-paper {
  font-size: 34px;
  padding: 5px;
  margin: 10px 0;
  border-radius: 10px;
}
</style>
