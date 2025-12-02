<template>
  <li>
    <div @click="toggleDetails" class="item-header">
      <p>
        {{ name }}
      </p>
      <p>
        {{ formattedPublicationDate }}
      </p>
      <p>
        {{ changes.length }}
      </p>

      <div class="controls">
        <button @click.stop="deleteArticle" class="delete-button">&#128465;</button>
        <span class="arrow">{{ isExpanded ? '&#9660;' : '&#9658;' }}</span>
      </div>
    </div>

    <div v-if="isExpanded" class="details-content">
      <slot name="details"></slot>
      <p v-if="content" v-html="formattedContent"></p>
      <DiffViewer v-for="(change, index) in changes" :key="index" :rawDiff="change.change" :changeId="change.id"
        :classification="change.classification" />
    </div>
  </li>
</template>

<script>
import DiffViewer from './diff_viewer.vue';

export default {
  name: 'Article',
  components: {
    DiffViewer
  },
  props: {
    name: {
      type: String,
      required: true
    },
    id: {
      type: [String, Number],
      required: true
    },
    content: {
      type: String,
      required: true
    },
    publication_date: {
      type: String,
      required: true
    },
    changes: {
      type: Array,
      default: () => []
    }
  },
  computed: {
    formattedContent() {
      return this.content ? this.content.replace(/\\n/g, '<br>') : '';
    },
    formattedPublicationDate() {
      if (!this.publication_date) return '';
      const date = new Date(this.publication_date);

      const day = String(date.getDate()).padStart(2, '0');
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const year = date.getFullYear();
      const hours = String(date.getHours()).padStart(2, '0');
      const minutes = String(date.getMinutes()).padStart(2, '0');
      return `${day}.${month}.${year} ${hours}:${minutes}`;
    }
  },
  data() {
    return {
      isExpanded: false,
    };
  },
  methods: {
    toggleDetails() {
      this.isExpanded = !this.isExpanded;
    },
    deleteArticle() {
      if (confirm('Are you sure you want to delete this article? This action cannot be undone.')) {
        fetch(`http://localhost:1000/api/data/articles/${this.id}`, {
          method: 'DELETE',
        })
          .then(response => {
            if (!response.ok) {
              throw new Error('Network response was not ok');
            }
            return response.json();
          })
          .then(data => {
            console.log('Article deleted:', data.message);
            this.$emit('article-deleted', this.id);
          })
          .catch(error => {
            console.error('Error deleting article:', error);
          });
      }
    }
  }
}
</script>

<style scoped>
li {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.item-header {
  display: grid;
  grid-template-columns: 12fr 4fr 2fr 2fr;
  gap: 10px;
  align-items: center;
  cursor: pointer;
  padding: 8px;
  border: 1px solid #ccc;
  margin-bottom: -1px;
  background-color: #f9f9f9;
}
.controls {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 15px;
}
.delete-button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.2em;
  color: firebrick;
}
.item-header .controls {
  justify-self: end;
}

.details-content {
  padding: 10px 8px;
  background-color: #eee;
  border: 1px solid #ccc;
}

.arrow {
  font-size: 1.2em;
  margin-left: 10px;
}
</style>
