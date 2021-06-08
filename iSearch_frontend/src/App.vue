<template>
  <div id="app">
    <router-view />
    <footer>
      <Icon type="logo-github" @click="goGithub()" class="footer-github" />
      <br />
      Copyright 2021 All rights reserved.
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App',
  methods: {
    goGithub() {
      window.open('https://github.com/jaingmengmeng/iSearch', '_blank');
    }
  }
};
</script>

<style lang="scss" scoped>
router-view {
  margin-bottom: 100px;
}
footer {
  background-color: white;
  width: 100%;
  height: 60px;
  position: static;
  bottom: 0;
  left: 0;
  text-align: center;
  font-size: 16px;
  z-index: 100;
  margin-top: 30px;
  .footer-github {
    font-size: 20px;
    cursor: pointer;
  }
}
</style>
