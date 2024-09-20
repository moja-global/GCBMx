<template>
        <div class="py-4 px-8 text-earth">
          <a-typography-title :level="2"><span class="font-normal text-earth"> Download </span></a-typography-title>
          <a-typography-text>
            <span class="text-earth mb-6 block">
              Download the output from the GCBM Simulation <br />
            </span
            >
          </a-typography-text>

          <div class="flex justify-items-center flex-row gap-2 mb-4">
            <a-typography-text>
              <span class=""> Active Simulation: </span>
            </a-typography-text>
            <a-typography-title :level="5" style="margin: 0">
              <span class="text-earth"> {{ simulation_title }} </span>
            </a-typography-title>
          </div>

          <div class="flex gap-4">

            <button
              class="
                hover:bg-earth hover:text-white
                text-gray-800
                font-semibold
                py-2
                px-4
                border border-gray-400
                rounded
                shadow
                flex
                items-center
                gap-2
              "
              @click="downloadSim"
            >
              <DownloadOutlined />
              <span class="whitespace-nowrap">Download GCBM Output</span>
            </button>
          </div>

          <div class="mt-4">
            <h3>logging:</h3>
            <div class="logs-container">
              <pre>{{ logs }}</pre>
            </div>
          </div>
          <ToastComponent />
        </div>
      </template>

      <script>
      import { useToast, ToastComponent } from '@moja-global/mojaglobal-ui'
      import {  DownloadOutlined } from '@ant-design/icons-vue'
      import { useStore } from 'vuex'
      import { ref } from 'vue';


      export default {
        name: 'GCBMDownload',
        components: {
          DownloadOutlined,
          ToastComponent
        },

        setup() {
          const store = useStore()
          const simulation_title = store.state.gcbm.config.title
          const logs = ref('')

          function downloadSim() {
            var bodyFormData = new FormData()
            bodyFormData.append('title', simulation_title)
            console.log(simulation_title)
            console.log([...bodyFormData])
            logs.value = 'Starting Download...\n';

            fetch(`${process.env.VUE_APP_REST_API_GCBM}/gcbm/download`, { method: 'POST', body: bodyFormData })
              .then((response) => response.blob())
              .then((bytes) => {
                console.log(bytes)
                const url = window.URL.createObjectURL(bytes)
                const link = document.createElement('a')
                link.href = url
                link.setAttribute('download', simulation_title + '_gcbm_run_ouput' + '.zip')
                document.body.appendChild(link)
                link.click()
              })
              .catch((error) => {
                useToast({
                  type: 'error',
                  title: 'Error',
                  message: `${error}`,
                  time: 5000
                })
                console.log(error)
              })
              logs.value = 'Download Complete...\n';
          }
          return { simulation_title,  downloadSim, logs }
        }
      }
      </script>

      <style>
      pre {
        background-color: #f8f8f8;
        padding: 10px;
        border: 1px solid #ddd;
        max-height: 400px;
        overflow-y: auto;
      }
      .logs-container {
        max-height: 400px;
        max-width: 500px;
        overflow-y: auto;
        background-color: #f4f4f9; /* Light grey background for better readability */
        border: 1px solid #03381d; /* Light border */
        padding: 10px;
        border-radius: 5px; /* Rounded corners */
        font-family: monospace; /* Monospace font for log-like appearance */
        white-space: pre-wrap; /* Ensure line breaks are preserved */
      }
      </style>