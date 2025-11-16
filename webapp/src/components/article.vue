<template>
  <li>
    <div @click="toggleDetails" class="item-header">
      <p>
        <strong>{{ id }}</strong> | {{ publication_date }} | {{ name }} | Changes: {{ changes.length }}
      </p>

      <span class="arrow">{{ isExpanded ? '&#9660;' : '&#9658;' }}</span>
    </div>

    <div v-if="isExpanded" class="details-content">
      <slot name="details"></slot>
      <p v-if="content" v-html="formattedContent"></p>
      <DiffViewer :rawDiff="change.change" v-for="(change, index) in changes" :key="index" />
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
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  padding: 8px;
  border: 1px solid #ccc;
  margin-bottom: -1px;
  background-color: #f9f9f9;
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
