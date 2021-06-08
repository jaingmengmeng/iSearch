<template>
  <div class="logo" @click="goIndex()">
    <img src="../assets/isearch-logo.png" />
  </div>
</template>

<script>
export default {
  name: 'Logo',
  data() {
    return {
      name: 'iSearch'
    };
  },
  methods: {
    goIndex() {
      this.$router.replace({
        name: 'Search',
        query: {}
      });
      this.$router.go(0);
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.logo {
  cursor: pointer;
  img {
    max-width: 360px;
    width: 100%;
    height: auto;
  }
}
</style>
