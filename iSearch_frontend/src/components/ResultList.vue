<template>
  <div class="result-list">
    <div class="search-res-list" v-for="(item, i) in doc_list" :key="i">
      <result
        :url="item.url"
        :abstract="item.abstract"
        :title="item.title"
      ></result>
    </div>
    <div align="center">
      <Page
        :total="doc_list_len"
        :page-size="page_size"
        :current="page_num"
        @on-change="handleChange"
        @on-page-size-change="handlePageSizeChange"
      ></Page>
    </div>
  </div>
</template>

<script>
import Result from './Result.vue';
export default {
  name: 'ResultList',
  props: ['doc_list', 'doc_list_len', 'page_size', 'page_num'],
  components: {
    Result
  },
  methods: {
    handleChange(page) {
      this.$emit('page_num', page);
    },
    handlePageSizeChange(size) {
      this.$emit('page_size', size);
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss"></style>
