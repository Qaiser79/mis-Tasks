<template>
    <Bar :data="chartData" :options="chartOptions"/>
</template>

<script>
import { Bar } from 'vue-chartjs'
import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    BarElement,
    CategoryScale,
    LinearScale
} from 'chart.js'

ChartJS.register(Title,Tooltip,Legend,BarElement,CategoryScale,LinearScale)

export default {
    name: 'MonthlyChart',
    props: {
        data: Object,
        options: Object
    },
    components: {Bar},
    computed: {
        chartData() {return this.data},
        chartOptions() {return this.options}
    }

}

</script>