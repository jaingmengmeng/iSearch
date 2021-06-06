// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue';
import App from './App';
import router from './router';
// iview ui framework
import iView from 'iview';
import 'iview/dist/styles/iview.css';
import Axios from 'axios';

Vue.config.productionTip = false;
Vue.use(iView);
Vue.prototype.$axios = Axios;
// Axios.defaults.headers.post['Content-Type'] = 'application/x-www-fromurlencodeed';

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
});
