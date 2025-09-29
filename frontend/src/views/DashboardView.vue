<template>
<div class="page-container">
    <header class="dashboard-header">
      <h1>MIS Dashboard</h1>
      <p>Track, manage, and update MIS records across departments in real time.</p>
    </header>

    <section class="card-section">
      <h2 class="section-title">MIS Summary</h2>
      <div class="dashboard-grid">
        <MISCountCard title="Total MIS" :count="misCount" bgColor="#007bff" iconClass="fas fa-tasks" />
        <MISCountCard title="Completed" :count="statusCounts.Completed || 0" bgColor="#28a745" iconClass="fas fa-check-circle" />
        <MISCountCard title="Pending" :count="statusCounts.Pending || 0" bgColor="#fd7e14" iconClass="fas fa-hourglass-half" />
        <MISCountCard title="In Progress" :count="statusCounts['In Progress'] || 0" bgColor="#6f42c1" iconClass="fas fa-spinner" />
        <MISCountCard title="UAT-ITG" :count="statusCounts['UAT-ITG'] || 0" bgColor="#20c997" iconClass="fas fa-laptop-code" />
        <MISCountCard title="UAT-USER" :count="statusCounts['UAT-USER'] || 0" bgColor="#6c757d" iconClass="fas fa-users" />
        <MISCountCard title="Cancelled" :count="statusCounts.Cancelled || 0" bgColor="#dc3545" iconClass="fas fa-times-circle" />
      </div>
    </section>

    <div class="chart-container">
        <StatusChart
            v-if="chartData.datasets[0].data.length > 0"
            :data="chartData"
            :options="chartOptions"
        />

        <MonthlyChart 
        v-if="monthlyChartData.datasets[0].data.length > 0"
        :data="monthlyChartData"
        :options="monthlyChartOptions"
      />

        <p v-else>Loading chart data...</p>
    
      
    </div>


  </div>
</template>
<script>
  import axios from 'axios'
  import StatusChart from '../components/StatusChart.vue'
  import MISCountCard from '../components/MISCountCard.vue'
  import MonthlyChart from '../components/MonthlyChart.vue'
  import { ref, onMounted } from 'vue'
  /*import Sidebar from '../components/Sidebar.vue'*/
  export default {
    components: { MISCountCard,StatusChart, MonthlyChart},
    data() {
    return {
      misCount: 0,
      statusCounts: {
        Completed:0,
        Pending: 0,
        'In Progress': 0,
        'UAT-ITG': 0,
        'UAT-USER': 0,
        Cancelled: 0
      },
      chartData: {
      labels: [],
      datasets: [{
        data: [],
        backgroundColor: ['#28a745', '#fd7e14', '#6f42c1', '#20c997', '#6c757d', '#dc3545']
      }]
      },
        chartOptions: {
            responsive: true,
                plugins: {
                    legend: {
                    position: 'bottom'
                    },
                    title: {
                    display: true,
                    text: 'MIS Status Breakdown'
                    }
                }
        },

        monthlyChartData: {
          labels: [],
          datasets: [{
            label: 'Monthly MIS Records',
            data: [],
            backgroundColor: '#0d6efd'
          }]
        },
        monthlyChartOptions: {
          responsive: true,
          plugins: {
            legend: { display: false },
            title: { display: true, text: 'Monthly MIS Trends' }
          }
        }

    }
    },
  methods: {
    async refreshMISCount(){
      const totalRes= await axios.get('http://127.0.0.1:8000/mis/count')
      this.misCount=totalRes.data.total_mis

      //status breakdown
      const statuses= ['Completed','Pending', 'In Progress', 'UAT-ITG', 'UAT-USER', 'Cancelled']
      for (const status of statuses){
        const res= await axios.get(`http://127.0.0.1:8000/mis/status-count?status=${encodeURIComponent(status)}`)
        //this.$set(this.statusCounts, status,res.data.count)
        this.statusCounts[status] = res.data.count

        
      }

      this.chartData.labels = Object.keys(this.statusCounts)
      this.chartData.datasets[0].data = Object.values(this.statusCounts)

      console.log('Updated statusCounts:', this.statusCounts)
    },

    async fetchMonthlyChart(){
      const res = await axios.get('http://localhost:8000/mis/monthly-count')
      const data = res.data

      this.monthlyChartData.labels=Object.keys(data)
      this.monthlyChartData.datasets[0].data= Object.values(data)
    }



  },
  mounted() {
    this.refreshMISCount();
    this.fetchMonthlyChart();
  }
}
</script>

<style scoped>

.page-container {
  width: 100%;
  padding: 30px 60px;
}

.dashboard-header {
  text-align: center;
  margin-bottom: 30px;
}

.dashboard-header h1 {
  font-size: 2rem;
  margin-bottom: 10px;
  color: #343a40;
}

.dashboard-header p {
  font-size: 1rem;
  color: #6c757d;
}

.section-title {
  font-size: 1.4rem;
  margin-bottom: 16px;
  color: #343a40;
}

.card-section {
  margin-bottom: 40px;
}




.dashboard-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-start;
  gap: 16px;
}

.chart-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 32px;
  margin: 40px 0;
  padding: 0 20px;
}

.chart-container canvas {
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  padding: 20px;
}

.chart-container h2 {
  font-size: 1.2rem;
  margin-bottom: 12px;
  color: #343a40;
  text-align: center;
}

</style>