<template>
  <div class="logo">
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
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.logo {
  img {
    max-width: 360px;
    width: 100%;
    height: auto;
  }
}
</style>
