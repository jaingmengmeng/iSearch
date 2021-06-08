<template>
  <div class="corrected-query">
    您要找的是不是：
    <div class="corrected-query-link" @click="updateQuery">
      {{ corrected_query }}
    </div>
  </div>
</template>

<script>
export default {
  name: 'CorrectedQuery',
  props: ['corrected_query'],
  data() {
    return {};
  },
  methods: {
    updateQuery() {
      this.$router.replace({
        name: 'Search',
        query: {
          q: this.corrected_query
        }
      });
      this.$router.go(0);
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.corrected-query {
  display: flex;
  .corrected-query-link {
    cursor: pointer;
    color: #1a0dab;
  }
}
</style>
