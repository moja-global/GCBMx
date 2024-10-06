<template>
        <div class="py-4 px-8 text-earth">
          <a-typography-title :level="2"><span class="font-normal text-earth"> Visualize </span></a-typography-title>
          <a-typography-text>
            <span class="text-earth mb-6 block">
              Visualize the spatial and aspatial outputs of the GCBM Simulation <br />
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
              @click="runViz"
            >
              <LineChartOutlined />
              <span class="whitespace-nowrap">Visualize with Taswira</span>
            </button>

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
              @click="runViz"
            >
              <LineChartOutlined />
              <span class="whitespace-nowrap">Visualize with GEE</span>
            </button>
          </div>

          <div class="mt-4">
            <h3>Visualization Logs:</h3>
            <div class="logs-container">
              <pre>{{ logs }}</pre>
            </div>
          </div>
          <ToastComponent />
        </div>
      </template>

      <script>
      import { useToast, ToastComponent } from '@moja-global/mojaglobal-ui'
      import { LineChartOutlined } from '@ant-design/icons-vue'
      import { useStore } from 'vuex'
      import { ref } from 'vue';


      export default {
        name: 'GCBMViz',
        components: {
          LineChartOutlined,
          ToastComponent
        },

        setup() {
          const store = useStore()
          const simulation_title = store.state.gcbm.config.title
          const logs = ref('')

          function fetchLogs(title) {
              const eventSource = new EventSource(`${process.env.VUE_APP_REST_API_GCBM}/gcbm/logs/${title}`);

              eventSource.onmessage = (event) => {
                  const data = event.data;
                  logs.value += data + '\n'; // Update the component's state with new data
              };

              eventSource.onerror = (error) => {
                  console.error('SSE error:', error);
                  // Optionally, handle error or reconnect logic
              };

              eventSource.onopen = () => {
                  console.log('SSE connection established.');
              };

              // Optionally handle the connection close
              eventSource.onclose = () => {
                  console.log('SSE connection closed.');
              };
          }

          function runViz() {
            var bodyFormData = new FormData()
            bodyFormData.append('title', simulation_title)
            console.log(simulation_title)
            console.log([...bodyFormData])

            fetch(`${process.env.VUE_APP_REST_API_VIZ}/viz`, { method: 'POST', body: bodyFormData })
              .then((response) => {
                console.log(response)
                if (response.status === 500) {
                  throw new Error('There was an error running the visualization. Please try again later.')
                } else {
                  return response.json()
                }
              })
              .then((response) => {
                console.log(response)
                useToast({
                  type: 'success',
                  title: 'Success',
                  message: response.status,
                  time: 5000
                })
              })
              .catch((error) => {
                useToast({
                  type: 'error',
                  title: 'error',
                  message: `${error}`,
                  time: 5000
                })
                console.log(error)
              })
          }




          return { simulation_title, runViz, logs, fetchLogs  }
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