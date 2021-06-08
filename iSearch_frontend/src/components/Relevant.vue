<template>
  <div class="relevant">
    相关搜索
    <br />
    <div
      class="relevant-list"
      v-for="(item, i) in relevant_list.slice(
        (page_num - 1) * page_size,
        page_num * page_size
      )"
      :key="i"
    >
      <div @click="updateURL(item)">{{ i + 1 }} {{ item }}</div>
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
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.relevant {
  color: #222;
  font: 18px Arial, sans-serif;
  font-weight: 400;
  line-height: 2;
  .relevant-list {
    cursor: pointer;
    max-width: 100%;
    color: #2440b3;
    font: 18px Arial, sans-serif;
    font-weight: 400;
    white-space: nowrap;
    text-overflow: ellipsis;
    overflow: hidden;
    vertical-align: middle;
    display: inline-block;
    -webkit-line-clamp: 1;
  }
  .relevant-list:hover {
    text-decoration: underline;
  }
}
</style>
