// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue';
import Vuetify from 'vuetify';
import Axios from 'axios';
import VueAxios from 'vue-axios';

import App from './App';
import router from './router';


Vue.config.productionTip = false;

Vue.use(Vuetify);
Vue.use(VueAxios, Axios);

require('vuetify/dist/vuetify.min.css');

Axios.defaults.baseURL = 'http://localhost:8080';

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>',
});
