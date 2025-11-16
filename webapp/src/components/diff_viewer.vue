<template>
  <div class="diff-viewer">
    <div class="diff-header">
      <span class="removed">--- {{ header.oldFile }}</span>
      <span class="added">+++ {{ header.newFile }}</span>
    </div>

    <div v-for="(line, index) in parsedDiff" :key="index" :class="['diff-line', line.type]">
      <span class="line-num old-num">{{ line.oldLineNum }}</span>
      <span class="line-num new-num">{{ line.newLineNum }}</span>
      
      <pre class="line-content">{{ line.content }}</pre>
    </div>
  </div>
</template>

<script>

export default {
  name: 'DiffViewer',
  props: {
    rawDiff: {
      type: String,
      required: true,
      default: ''
    }
  },
  data() {
    return {
      // Initialize header data
      header: {
        oldFile: 'Original File',
        newFile: 'New File'
      }
    };
  },
  computed: {
    parsedDiff() {
      // 1. Split the raw diff text into individual lines
      const lines = this.rawDiff.split('\n').filter(l => l.length > 0);
      const output = [];
      let oldLineCounter = 0;
      let newLineCounter = 0;

      for (const line of lines) {
        let type = 'context'; // default type is unchanged

        if (line.startsWith('--- ')) {
          this.header.oldFile = line.substring(4);
          continue; // Skip the line
        }
        if (line.startsWith('+++ ')) {
          this.header.newFile = line.substring(4);
          continue; // Skip the line
        }

        // 2. Identify the type and content based on the first character
        if (line.startsWith('@@')) {
          type = 'hunk-header';
          // Reset line counters based on the hunk header
          // The format is @@ -oldStart,oldCount +newStart,newCount @@
          const match = line.match(/@@ -(\d+),\d+ \+(\d+),\d+ @@/);
          if (match) {
            oldLineCounter = parseInt(match[1]) - 1; // -1 because it increments *before* content lines
            newLineCounter = parseInt(match[2]) - 1; 
          }
        } else if (line.startsWith('-')) {
          type = 'removed';
          oldLineCounter++;
        } else if (line.startsWith('+')) {
          type = 'added';
          newLineCounter++;
        } else {
          // Unchanged line
          oldLineCounter++;
          newLineCounter++;
        }

        // 3. Store the structured line data
        output.push({
          type,
          content: type === 'hunk-header' ? line : line.substring(1), // Remove the +/-/space prefix
          oldLineNum: ['removed', 'context'].includes(type) ? oldLineCounter : '',
          newLineNum: ['added', 'context'].includes(type) ? newLineCounter : ''
        });
      }

      return output;
    }
  }
}
</script>

<style scoped>
/* Main container for the diff */
.diff-viewer {
  font-family: monospace;
  font-size: 14px;
  line-height: 1.4;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 4px;
  overflow:auto;
  width: 100%;
}

/* Header for file names */
.diff-header {
  padding: 8px 15px;
  background-color: #f0f0f0;
  border-bottom: 1px solid #ddd;
  font-weight: bold;
}
.diff-header .removed { color: firebrick; margin-right: 20px; }
.diff-header .added { color: green; }

/* Individual line styling */
.diff-line {
  display: flex;
  white-space: pre-wrap;
  align-items: flex-start;
  width: 100%;
  margin: 0;
}

/* Line Number Columns */
.line-num {
  width: 40px;
  padding: 0 10px;
  text-align: right;
  color: #777;
  background-color: #f7f7f7;
  border-right: 1px solid #eee;
  box-sizing: border-box;
}

/* Content Column */
.line-content {
  flex-grow: 1;
  padding: 0 10px;
  margin: 0;
  white-space: pre; /* preserve whitespace */
  display: block;
}

/* Specific styling for line types - target the same element that has both classes */
.diff-line.removed { background-color: #ffeef0; } /* Light red/pink */
.diff-line.removed .line-num { color: firebrick; background-color: #ffeef0; }
.diff-line.removed .line-content { color: firebrick; }

.diff-line.added { background-color: #e6ffed; } /* Light green */
.diff-line.added .line-num { color: green; background-color: #e6ffed; }
.diff-line.added .line-content { color: green; }

.diff-line.context { background-color: #fff; }
.diff-line.hunk-header { 
  background-color: #f7f7f7; 
  color: #777;
  font-style: italic;
  font-weight: bold;
}
.diff-line.hunk-header .line-num { background-color: #e0e0e0; color: #777; }
</style>