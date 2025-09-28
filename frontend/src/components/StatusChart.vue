<template>
    <Doughnut :data="chartData" :options="chartOptions" />
</template>
  
  <script>
  import { Doughnut } from 'vue-chartjs'
  import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    ArcElement
  } from 'chart.js'
  
  ChartJS.register(Title, Tooltip, Legend, ArcElement)
  
  export default {
    name: 'StatusChart',
    props: {
      data: Object,
      options: Object
    },
    components: {
      Doughnut
    },
    computed: {
      chartData() {
        return this.data
      },
      chartOptions() {
        return this.options
      }
    }
  }
  </script>
  