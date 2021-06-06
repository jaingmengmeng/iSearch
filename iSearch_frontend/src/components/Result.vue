<template>
  <div class="result">
    <div class="result-title" @click="goto()">
      {{ title }}
    </div>
    <div class="result-abstract">
      {{ abstract }}
    </div>
  </div>
</template>

<script>
export default {
  name: 'Result',
  props: ['title', 'abstract', 'url'],
  methods: {
    goto() {
      window.open(this.url, '_blank');
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.result {
  margin-bottom: 30px;
  .result-title {
    font-size: 20px;
    font-family: arial, sans-serif;
    font-weight: normal;
    color: #1a0dab;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    cursor: pointer;
  }
  .result-title:hover {
    text-decoration: underline;
    // color: #1a0dab;
  }
  .result-abstract {
    font-size: 14px;
    font-family: arial, sans-serif;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    word-wrap: break-word;
    word-break: break-all;
  }
}
</style>
