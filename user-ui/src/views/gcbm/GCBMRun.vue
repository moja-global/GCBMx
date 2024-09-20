<template>
  <div class="py-4 px-8 text-earth">
    <a-typography-title :level="2"><span class="font-normal text-earth"> Run </span></a-typography-title>
    <a-typography-text>
      <span class="text-earth mb-6 block">
        Run the simulation on the configured parameters. <br />
        You can also <a-typography-link @click="exportSim">export the simulation</a-typography-link> and continue
        editing later.</span
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
       v-if="simulationRunning"
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
        @click="runit"
      >
        <PlayCircleOutlined />
        <span class="whitespace-nowrap">Run simulation</span>
      </button>

      <button
       v-if="simulationRunning"
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
        @click="checkStatus"
      >
        <QuestionCircleOutlined :style="{ fontSize: '16px' }" />
        <span>Check status</span>
      </button>

      <button
       v-if="!simulationRunning"
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
        <DownloadOutlined />
        <span class="whitespace-nowrap">Visualize GCBM results</span>
      </button>

      <button
       v-if="!simulationRunning"
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

    <div v-if="simulationRunning" class="mt-4">
      <h3>GCBM Simulation Logs:</h3>
      <div class="logs-container">
        <pre>{{ logs }}</pre>
      </div>
    </div>
    <ToastComponent />
  </div>
</template>

<script>
import { useToast, ToastComponent } from '@moja-global/mojaglobal-ui'
import { PlayCircleOutlined, DownloadOutlined, QuestionCircleOutlined } from '@ant-design/icons-vue'
import { useStore } from 'vuex'
import * as JSZip from 'jszip'
import { saveAs } from 'file-saver'
import { ref } from 'vue';


export default {
  name: 'GCBMRun',
  components: {
    PlayCircleOutlined,
    DownloadOutlined,
    QuestionCircleOutlined,
    ToastComponent
  },

  setup() {
    const store = useStore()
    const simulation_title = store.state.gcbm.config.title
    const simulationRunning = ref(true);
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


    async function runit() {
      this.runSim();
      this.fetchLogs(this.simulation_title);
    }

    function runSim() {
      var bodyFormData = new FormData()
      bodyFormData.append('title', simulation_title)
      console.log(simulation_title)
      console.log([...bodyFormData])
      logs.value = 'Starting simulation...\n';

      fetch(`${process.env.VUE_APP_REST_API_GCBM}/gcbm/dynamic`, { method: 'POST', body: bodyFormData })
        .then((response) => {
          console.log(response)
          if (response.status === 500) {
            throw new Error('There was an error running the simulation. Please try again later.')
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

    function runViz() {
      var bodyFormData = new FormData()
      bodyFormData.append('title', simulation_title)
      console.log(simulation_title)
      console.log([...bodyFormData])

      fetch(`${process.env.VUE_APP_REST_API_VIZ}/viz`, { method: 'POST', body: bodyFormData })
        .then((response) => {
          console.log(response)
          if (response.status === 500) {
            throw new Error('There was an error running the simulation. Please try again later.')
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


    function checkStatus() {
      var bodyFormData = new FormData()
      bodyFormData.append('title', simulation_title)

      fetch(`${process.env.VUE_APP_REST_API_GCBM}/gcbm/status`, { method: 'POST' })
        .then((response) => response.json())
        .then((data) => {
          useToast({
            type: 'info',
            title: 'Info',
            message: `${data.finished}`,
            time: 5000
          })
          console.log(data.finished)
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
    }

    function exportSim() {
      const zip = new JSZip()
      const simFolder = zip.folder(simulation_title)
      const config = simFolder.folder('config')
      config.file('localdomain.json', JSON.stringify(store.state.gcbm.config.localdomain, null, 2))
      config.file('modules_cbm.json', JSON.stringify(store.state.gcbm.config.modules_cbm, null, 2))
      config.file('pools_cbm.json', JSON.stringify(store.state.gcbm.config.pools_cbm, null, 2))
      config.file('spinup.json', JSON.stringify(store.state.gcbm.config.spinup, null, 2))
      config.file('variables.json', JSON.stringify(store.state.gcbm.config.variables, null, 2))
      config.file('internal_variables.json', JSON.stringify(store.state.gcbm.config.internal_variables, null, 2))

      zip.generateAsync({ type: 'blob' }).then((content) => {
        saveAs(content, simulation_title + '.zip')
      })
    }

    return { simulation_title, runit, runSim, checkStatus, exportSim, runViz, logs, fetchLogs, simulationRunning  }
  }
}
</script>

<style>
.logs-container {
  flex: 1;
  height: 50vh;
  width: 90vw;
  overflow-y: auto;
  background-color: #f4f4f9; /* Light grey background for better readability */
  border: 1px solid #03381d; /* Light border */
  padding: 10px;
  border-radius: 5px; /* Rounded corners */
  font-family: monospace; /* Monospace font for log-like appearance */
  white-space: pre-wrap; /* Ensure line breaks are preserved */
}
</style>