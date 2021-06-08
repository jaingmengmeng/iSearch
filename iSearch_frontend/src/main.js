// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue';
import App from './App';
import router from './router';
// iview ui framework
import ViewUI from 'view-design';
import 'view-design/dist/styles/iview.css';
// axios
import Axios from 'axios';

Vue.config.productionTip = false;
Vue.use(ViewUI);
Vue.prototype.$axios = Axios;
// Axios.defaults.headers.post['Content-Type'] = 'application/x-www-fromurlencodeed';

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
});
