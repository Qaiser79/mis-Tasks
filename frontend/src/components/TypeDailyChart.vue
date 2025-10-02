<template>
    <Line :data="chartData" :options="chartOptions"/>
</template>

<script>
    import {Line} from 'vue-chartjs'
    import{
        Chart as ChartJS,
        Title,
        Tooltip,
        Legend,
        LineElement,
        PointElement,
        CategoryScale,
        LinearScale,
        Filler
    } from 'chart.js'

    ChartJS.register(
        Title,
        Tooltip,
        Legend,
        LineElement,
        PointElement,
        CategoryScale,
        LinearScale,
        Filler
    )

    export default {
        name: 'TypeDailyChart',
        props: {
            data: Object,
            options: Object
        },
        components: {
            Line
        },
        computed: {
            chartData(){
                return this.data
            },
            chartOptions(){
                return this.options
            }
        }
    }
        
</script>