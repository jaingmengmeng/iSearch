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
      <div class="search-res-affix">
        <Affix>
          <span class="affix">
            <Row type="flex" class="search-res-row" align="middle">
              <Col
                :xs="{ span: 18, offset: 3 }"
                :sm="{ span: 18, offset: 3 }"
                :md="{ span: 4, offset: 0 }"
                :lg="{ span: 4, offset: 0 }"
                class="search-res-col"
              >
                <logo class="logo"></logo>
              </Col>
              <Col
                :xs="{ span: 20, offset: 2 }"
                :sm="{ span: 20, offset: 2 }"
                :md="{ span: 16, offset: 0 }"
                :lg="{ span: 12, offset: 0 }"
                class="search-res-col"
              >
                <search-bar
                  class="search-bar"
                  :q="query"
                  @query="updateQuery"
                ></search-bar>
              </Col>
            </Row>
          </span>
        </Affix>
      </div>
      <result-list
        :doc_list="doc_list"
        :page_num="page_num"
        :page_size="page_size"
        @page_num="updatePageNum"
        @page_size="updatePageSize"
      ></result-list>
    </div>
  </div>
</template>
<script>
import Logo from '../components/Logo.vue';
import SearchBar from '../components/SearchBar.vue';
import ResultList from '../components/ResultList.vue';
export default {
  name: 'Search',
  components: {
    Logo,
    SearchBar,
    ResultList
  },
  data() {
    return {
      query: '',
      page_size: 10,
      page_num: 1,
      doc_list: []
    };
  },
  created: function() {
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
        this.updateURL();
      }
    }
  },
  mounted: async function() {
    await this.getResult();
  },
  watch: {
    query: 'getResult'
  },
  methods: {
    async getResult() {
      await this.$axios
        .get('/api/search/', {
          params: {
            q: this.query
          }
        })
        .then(res => {
          this.doc_list = res.data;
        })
        .catch(function(error) {
          console.log(error);
        });
    },
    async updateQuery(q) {
      if (this.query !== q) {
        this.query = q;
        this.page_size = 10;
        this.page_num = 1;
        this.updateURL();
      }
      await this.getResult();
    },
    updatePageNum(num) {
      this.page_num = num;
      this.updateURL();
    },
    updatePageSize(size) {
      this.page_size = size;
      this.updateURL();
    },
    updateURL() {
      this.$router.replace({
        name: 'Search',
        query: {
          q: this.query,
          page_size: this.page_size,
          page_num: this.page_num
        }
      });
    }
  }
};
</script>
<style scoped lang="scss">
.search {
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
  margin-bottom: 50px;
  .search-res-affix {
    background-color: white;
    .affix {
      .search-res-row {
        .search-res-col {
          .logo {
            text-align: center;
            margin-top: 20px;
            margin-left: 10%;
            margin-right: 10%;
            margin-bottom: 20px;
          }
          .search-bar {
            padding-top: 20px;
            padding-bottom: 20px;
          }
        }
      }
    }
  }
}
</style>
