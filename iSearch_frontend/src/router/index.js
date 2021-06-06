import Vue from 'vue';
import Router from 'vue-router';
import HelloWorld from '../pages/HelloWorld';
import Search from '../pages/Search';

Vue.use(Router);

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/search',
      name: 'Search',
      component: Search
    },
    {
      path: '/vue',
      name: 'HelloWorld',
      component: HelloWorld
    }
  ]
});
