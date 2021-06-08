<template>
  <div class="relevant" v-if="relevant_list.length > 0">
    <div class="relevant-header">
      相关搜索
      <div class="relevant-refresh" @click="Refresh()">
        <Icon type="ios-refresh" class="relevant-refresh-icon" />
        换一换
      </div>
    </div>
    <br />
    <div
      class="relevant-list"
      v-for="(item, i) in relevant_list.slice(
        (page_num - 1) * page_size,
        page_num * page_size
      )"
      :key="i"
    >
      <div @click="updateURL(item)" class="relevant-list-item">
        {{ i + 1 + (page_num - 1) * page_size }} {{ item }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Relevant',
  props: ['relevant_list'],
  data() {
    return {
      page_size: 7,
      page_num: 1
    };
  },
  methods: {
    updateURL(query) {
      this.$router.replace({
        name: 'Search',
        query: {
          q: query
        }
      });
      this.$router.go(0);
    },
    Refresh() {
      this.page_num =
        (this.page_num %
          Math.ceil(this.relevant_list.length / this.page_size)) +
        1;
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.relevant {
  .relevant-header {
    color: #222;
    font: 18px Arial, sans-serif;
    font-weight: 400;
    line-height: 2;
    .relevant-refresh {
      float: right;
      cursor: pointer;
      font: 14px Arial, sans-serif;
      color: #2440b3;
      font-weight: 400;
      line-height: 36px;
      .relevant-refresh-icon {
        font-size: 18px;
        line-height: 2;
      }
    }
  }
  .relevant-list {
    cursor: pointer;
    width: 100%;
    color: #2440b3;
    font: 18px Arial, sans-serif;
    font-weight: 400;
    line-height: 2;
    .relevant-list-item {
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
  }
  .relevant-list:hover {
    text-decoration: underline;
  }
}
</style>
