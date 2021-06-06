<template>
  <div class="result-list">
    <Row type="flex" class="search-row">
      <Col
        :xs="{ span: 20, offset: 2 }"
        :sm="{ span: 20, offset: 2 }"
        :md="{ span: 16, offset: 4 }"
        :lg="{ span: 12, offset: 4 }"
        class="search-col"
      >
        <div
          class="search-res-list"
          v-for="(item, i) in doc_list.slice(
            (page_num - 1) * page_size,
            page_num * page_size
          )"
          :key="i"
        >
          <result
            :url="item.url"
            :abstract="item.abstract"
            :title="item.title"
          ></result>
        </div>
        <div align="center">
          <Page
            :total="doc_list.length"
            :page-size="page_size"
            :current="page_num"
            @on-change="handleChange"
            @on-page-size-change="handlePageSizeChange"
          ></Page>
        </div>
      </Col>
    </Row>
  </div>
</template>

<script>
import Result from './Result.vue';
export default {
  name: 'ResultList',
  props: ['doc_list', 'page_size', 'page_num'],
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
