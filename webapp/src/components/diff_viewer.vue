<template>
  <div class="diff-viewer">
    <div class="diff-header">
      <div class="file-names">
        <span class="removed">--- {{ header.oldFile }}</span>
        <span class="added">+++ {{ header.newFile }}</span>
      </div>
      <div class="classification-control">
        <label :for="'classification-select-' + changeId">Classify:</label>
        <select :id="'classification-select-' + changeId" v-model="currentClassification"
          @change="updateClassification">
          <option value="not classified">Not Classified</option>
          <option value="typo">Typo</option>
          <option value="content change">Content Change</option>
        </select>
      </div>
    </div>

    <div v-for="(line, index) in parsedDiff" :key="index" :class="['diff-line', line.type]">
      <span class="line-num old-num">{{ line.oldLineNum }}</span>
      <span class="line-num new-num">{{ line.newLineNum }}</span>

      <pre class="line-content"><template v-for="(segment, segIndex) in line.content" :key="segIndex"><span :class="{ 'highlight': segment.highlighted }">{{ segment.text }}</span></template>
</pre>
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
    },
    changeId: {
      type: Number,
      required: true
    },
    classification: {
      type: String,
      required: true,
      default: 'not classified'
    }
  },
  data() {
    return {
      // Initialize header data
      currentClassification: this.classification,
      header: {
        oldFile: 'Original File',
        newFile: 'New File'
      }
    };
  },
  computed: {
    parsedDiff() {
      const lines = this.rawDiff.split('\n');
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

        if (type !== 'hunk-header') {
          // 3. Store the structured line data
          output.push({
            type,
            content: line,
            oldLineNum: ['removed', 'context'].includes(type) ? oldLineCounter : '',
            newLineNum: ['added', 'context'].includes(type) ? newLineCounter : ''
          });
        }
      }

      // Post-process to find and highlight intra-line diffs
      const finalOutput = [];
      for (let i = 0; i < output.length; i++) {
        const currentLine = output[i];
        const nextLine = (i + 1 < output.length) ? output[i + 1] : null;

        if (currentLine.type === 'removed' && nextLine && nextLine.type === 'added') {
          const { oldContent, newContent } = this.highlightIntralineDiff(currentLine.content, nextLine.content);
          currentLine.content = oldContent;
          nextLine.content = newContent;
          finalOutput.push(currentLine);
          finalOutput.push(nextLine);
          i++; // Skip next line as it has been processed
        } else {
          currentLine.content = [{ text: currentLine.content, highlighted: false }];
          finalOutput.push(currentLine);
        }
      }

      return finalOutput;
    }
  },
  methods: {
    highlightIntralineDiff(oldStr, newStr) {
      let start = 0;
      while (start < oldStr.length && start < newStr.length && oldStr[start] === newStr[start]) {
        start++;
      }

      let endOld = oldStr.length;
      let endNew = newStr.length;
      while (endOld > start && endNew > start && oldStr[endOld - 1] === newStr[endNew - 1]) {
        endOld--;
        endNew--;
      }

      const oldContent = [{ text: oldStr.substring(0, start), highlighted: false }, { text: oldStr.substring(start, endOld), highlighted: true }, { text: oldStr.substring(endOld), highlighted: false }];
      const newContent = [{ text: newStr.substring(0, start), highlighted: false }, { text: newStr.substring(start, endNew), highlighted: true }, { text: newStr.substring(endNew), highlighted: false }];
      return { oldContent, newContent };
    },
    updateClassification() {
      fetch(`http://localhost:1000/api/data/changes/${this.changeId}/classify`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ classification: this.currentClassification }),
      })
        .then(response => {
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          return response.json();
        })
        .then(data => {
          console.log('Classification updated:', data);
        })
        .catch(error => {
          console.error('Error updating classification:', error);
        });
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
  overflow: auto;
  width: 100%;
}

/* Header for file names */
.diff-header {
  padding: 8px 15px;
  background-color: #f0f0f0;
  border-bottom: 1px solid #ddd;
  font-weight: bold;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.file-names {
  display: flex;
  gap: 20px;
}

.classification-control select {
  padding: 4px;
  border-radius: 4px;
}

.diff-header .removed {
  color: firebrick;
}

.diff-header .added {
  color: green;
}

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
  white-space: pre-wrap;
  display: block;
}

.line-content .highlight {
  background-color: #f8eec7;
}

.diff-line.removed {
  background-color: #ffeef0;
}

/* Light red/pink */
.diff-line.removed .line-num {
  color: firebrick;
  background-color: #ffeef0;
}

.diff-line.removed .line-content .highlight {
  background-color: #fdb8c0;
  /* Darker red highlight */
  color: firebrick;
}

.diff-line.added {
  background-color: #e6ffed;
}

/* Light green */
.diff-line.added .line-num {
  color: green;
  background-color: #e6ffed;
}

.diff-line.added .line-content {
  color: green;
}

.diff-line.context {
  background-color: #fff;
}

.diff-line.hunk-header {
  background-color: #f7f7f7;
  color: #777;
  font-style: italic;
  font-weight: bold;
}

.diff-line.hunk-header .line-num {
  background-color: #e0e0e0;
  color: #777;
}

.diff-line.added .line-content .highlight {
  background-color: #abf2bc;
  color: green;
}
</style>