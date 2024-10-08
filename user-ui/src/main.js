import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'

import App from './App.vue'
import './index.css'

import { store } from './store'
import routes from './router/routes'

import OpenLayersMap from 'vue3-openlayers'
import 'vue3-openlayers/dist/vue3-openlayers.css'

import VueApexCharts from 'vue3-apexcharts'

import Vue3Tour from 'vue3-tour'
import 'vue3-tour/dist/vue3-tour.css'

import Antd from 'ant-design-vue'
import 'ant-design-vue/dist/reset.css'

// configure router
const router = createRouter({
  history: createWebHistory(),
  routes
})

const app = createApp(App)
app.use(Antd)
app.use(store)
app.use(router)
app.use(Vue3Tour)
app.use(VueApexCharts)
app.use(OpenLayersMap)

app.mount('#app')
