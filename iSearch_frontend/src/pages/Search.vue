<template>
  <div>
    <div class="search" v-if="query === ''">
      <Row type="flex" justify="center" class="search-row">
        <Col :xs="18" :sm="18" :md="12" :lg="12" class="search-col">
          <logo class="logo"></logo>
        </Col>
      </Row>
      <Row type="flex" justify="center" class="search-row">
        <Col :xs="20" :sm="20" :md="12" :lg="12" class="search-col">
          <search-bar class="search-bar" @query="updateQuery"></search-bar>
        </Col>
      </Row>
    </div>
    <div class="search-res" v-else>
      <Row class="search-res-header" type="flex" align="middle">
        <Col
          :xs="{ span: 18, offset: 3 }"
          :sm="{ span: 18, offset: 3 }"
          :md="{ span: 4, offset: 0 }"
          :lg="{ span: 4, offset: 0 }"
          class="search-res-logo"
        >
          <logo class="logo"></logo>
        </Col>
        <Col
          :xs="{ span: 20, offset: 2 }"
          :sm="{ span: 20, offset: 2 }"
          :md="{ span: 16, offset: 0 }"
          :lg="{ span: 12, offset: 0 }"
          class="search-res-search-bar"
        >
          <search-bar
            class="search-bar"
            :q="query"
            @query="updateQuery"
          ></search-bar>
        </Col>
      </Row>
      <Row class="search-res-content" type="flex" align="top">
        <Col
          :xs="{ span: 20, offset: 2 }"
          :sm="{ span: 20, offset: 2 }"
          :md="{ span: 16, offset: 4 }"
          :lg="{ span: 12, offset: 4 }"
        >
          <corrected-query
            class="corrected-query"
            v-if="corrected_query !== query"
            :corrected_query="corrected_query"
          ></corrected-query>
          <result-list
            class="result-list"
            v-if="doc_list_len > 0"
            :doc_list="doc_list"
            :doc_list_len="doc_list_len"
            :page_num="page_num"
            :page_size="page_size"
            @page_num="updatePageNum"
            @page_size="updatePageSize"
          ></result-list>
          <div class="blank" v-else>未查找到与 - {{ query }} - 相关的文档</div>
        </Col>
        <Col
          :xs="{ span: 20, offset: 2 }"
          :sm="{ span: 20, offset: 2 }"
          :md="{ span: 16, offset: 4 }"
          :lg="{ span: 6, offset: 1 }"
        >
          <relevant
            class="relevant-list"
            :relevant_list="relevant_list"
            ref="relevant"
          ></relevant>
        </Col>
      </Row>
    </div>
  </div>
</template>
<script>
import Logo from '../components/Logo.vue';
import SearchBar from '../components/SearchBar.vue';
import ResultList from '../components/ResultList.vue';
import Relevant from '../components/Relevant.vue';
import CorrectedQuery from '../components/CorrectedQuery.vue';
export default {
  name: 'Search',
  components: {
    Logo,
    SearchBar,
    ResultList,
    Relevant,
    CorrectedQuery
  },
  data() {
    return {
      query: '',
      page_size: 10,
      page_num: 1,
      corrected_query: '',
      doc_list: [],
      doc_list_len: 0,
      relevant_list: []
    };
  },
  created: async function() {
    if (this.$route.query.page_size !== undefined) {
      this.page_size = Number(this.$route.query.page_size);
    }
    if (this.$route.query.page_num !== undefined) {
      this.page_num = Number(this.$route.query.page_num);
    }
    if (this.$route.query.q !== undefined) {
      this.query = this.$route.query.q;
      if (
        this.$route.query.page_size === undefined ||
        this.$route.query.page_num === undefined
      ) {
        await this.updateURL();
      }
    }
  },
  mounted: async function() {
    if (this.query !== '') {
      await this.getResult();
    }
  },
  watch: {
    query: 'updateQuery'
  },
  methods: {
    async getResult() {
      this.$Spin.show({
        render: h => {
          return h('div', [
            h('Icon', {
              class: 'demo-spin-icon-load',
              props: {
                type: 'ios-loading',
                size: 20
              }
            }),
            h('div', 'Loading')
          ]);
        }
      });
      await this.$axios
        .get('/api/search/', {
          params: {
            q: this.query.trim(),
            page_size: this.page_size,
            page_num: this.page_num
          }
        })
        .then(res => {
          this.corrected_query = res.data.corrected_query;
          this.doc_list = res.data.doc_list;
          this.doc_list_len = res.data.doc_list_len;
          this.relevant_list = res.data.relevant_list;
          this.$Spin.hide();
        })
        .catch(function() {
          this.corrected_query = '';
          this.doc_list = [];
          this.doc_list_len = 0;
          this.relevant_list = [];
        });
    },
    async updateQuery(q) {
      if (this.query !== q) {
        this.query = q;
        this.page_size = 10;
        this.page_num = 1;
        await this.updateURL();
      } else {
        await this.getResult();
      }
    },
    async updatePageNum(num) {
      this.page_num = num;
      await this.updateURL();
    },
    async updatePageSize(size) {
      this.page_size = size;
      await this.updateURL();
    },
    async updateURL() {
      this.$router.replace({
        name: 'Search',
        query: {
          q: this.query,
          page_size: this.page_size,
          page_num: this.page_num
        }
      });
      await this.getResult();
      this.$refs.relevant.updatePageNum();
    }
  }
};
</script>
<style scoped lang="scss">
.search {
  min-height: calc(100vh - 90px);
  .search-row {
    .search-col {
      display: flex;
      align-items: center;
      justify-content: center;
      .logo {
        text-align: center;
        margin-top: 130px;
        margin-bottom: 38px;
      }
    }
  }
}
.search-res {
  min-height: calc(100vh - 90px);
  .search-res-header {
    background-color: white;
    width: 100%;
    height: fit-content;
    position: sticky;
    top: 0;
    left: 0;
    z-index: 100;
    box-shadow: 0 5px 5px -6px rgba(0, 0, 0, 0.5);
    .search-res-logo {
      text-align: center;
      margin-top: 20px;
      padding-left: 20px;
      padding-right: 20px;
      margin-bottom: 20px;
    }
    .search-res-search-bar {
      padding-top: 20px;
      padding-bottom: 20px;
    }
  }
  .blank,
  .corrected-query,
  .result-list,
  .relevant-list {
    margin-top: 30px;
  }
}
.demo-spin-icon-load {
  animation: ani-demo-spin 1s linear infinite;
}
@keyframes ani-demo-spin {
  from {
    transform: rotate(0deg);
  }
  50% {
    transform: rotate(180deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
