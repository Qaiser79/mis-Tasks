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
        <!--
        <MISCountCard title="UAT-ITG" :count="statusCounts['UAT-ITG'] || 0" bgColor="#20c997" iconClass="fas fa-laptop-code" />
        <MISCountCard title="UAT-USER" :count="statusCounts['UAT-USER'] || 0" bgColor="#6c757d" iconClass="fas fa-users" />
        <MISCountCard title="Cancelled" :count="statusCounts.Cancelled || 0" bgColor="#dc3545" iconClass="fas fa-times-circle" />
        -->
      </div>
    </section>

    <div class="chart-container">
      <div class="chart-box">
        <StatusChart
            v-if="chartData.datasets[0].data.length > 0"
            :data="chartData"
            :options="chartOptions"
        />
        </div>

        <div class="chart-box">
        <MonthlyChart 
        v-if="monthlyChartData.datasets[0].data.length > 0"
        :data="monthlyChartData"
        :options="monthlyChartOptions"
        />
      </div>

      <div class="month-selector">
          <label for="month">Select Month (default: September):</label>
            <select id="month" v-model="selectedMonth" >
              <option v-for="(name, index) in monthNames" :key="index" :value="index + 1">
                {{ name }}
              </option>
            </select>
      </div>


        <div class="chart-box">
          <MonthlyChart
            v-if="resourceChartData.datasets[0].data.length > 0"
            :data="resourceChartData"
            :options="resourceChartOptions"
          />
      </div>

        <div class="chart-box">
          <TypeDailyChart
            v-if="typeDailyChartData.datasets.length > 0"
            :data="typeDailyChartData"
            :options="typeDailyChartOptions"
          />
        </div>

      
    </div>


  </div>
</template>
<script>
  import axios from 'axios'
  import StatusChart from '../components/StatusChart.vue'
  import MISCountCard from '../components/MISCountCard.vue'
  import MonthlyChart from '../components/MonthlyChart.vue'
  import TypeDailyChart from '../components/TypeDailyChart.vue'
  import { ref, onMounted } from 'vue'
  /*import Sidebar from '../components/Sidebar.vue'*/
  export default {
    components: { MISCountCard,StatusChart, MonthlyChart,TypeDailyChart},
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
                    position: 'right'
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
        },

        resourceChartData:{
          labels: [],
            datasets: [{
              label: 'MIS Records by Resource',
              data: [],
              backgroundColor: []
            }]
        },

        resourceChartOption: {
          responsive: true,
              plugins: {
                legend: { display: false },
                title: { display: true, text: 'Resource-wise MIS Distribution' }
              },
              scales: {
                y: {
                  beginAtZero: true,
                  ticks: {
                    stepSize: 1
                  }
                }
              }

        },

        typeDailyChartData: {
            labels: [],
            datasets: []
        },
        typeDailyChartOptions: {
            responsive: true,
            plugins: {
              title: { display: true, text: 'Daily MIS Type Trend' },
              legend: { display: true },
            },
            scales: {
                y: {
                  beginAtZero: true,
                  ticks: {
                    precision: 0 // ✅ removes .0 decimals
                  }
                },
                x: {
                  ticks: {
                    autoSkip: false,
                    maxRotation: 0,
                    minRotation: 0
                  }
                }
}
        },

        selectedMonth: 9,
          monthNames: [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
          ],


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
    },
    async fetchResourceChart(month){
      const res = await axios.get(`http://127.0.0.1:8000/mis/by-resource?month=${month}`)
      const data = res.data

      const labels = Object.keys(data)
      const values = Object.values(data)

      // Generate a unique color for each resource
      const colors = labels.map((_, i) => {
        const palette = ['#20c997', '#0d6efd', '#fd7e14', '#6f42c1', '#28a745', '#dc3545', '#6c757d']
        return palette[i % palette.length] // cycle through palette
      })

      this.resourceChartData = {
      labels,
      datasets: [{
        label: 'MIS Records by Resource',
        data: values,
        backgroundColor: colors
          }]
        }
    },
    async fetchTypeDailyChart(month) {
        const res = await axios.get(`http://127.0.0.1:8000/mis/type_daily_trend?month=${month}`)
        const data = res.data

        // Step 1: Collect all unique dates
        const allDatesSet = new Set()
        Object.values(data).forEach(dateMap => {
          Object.keys(dateMap).forEach(date => allDatesSet.add(date))
        })

        const rawDates = Array.from(allDatesSet).sort()

        // Step 2: Format labels for display
        const displayLabels = rawDates.map(dateStr => {
          const parsed = Date.parse(dateStr)
          return !isNaN(parsed)
            ? new Date(parsed).toLocaleDateString('en-US', { weekday: 'short', day: 'numeric' })
            : dateStr
        })

        // Step 3: Build datasets per mis_type
        const types = Object.keys(data)
        const palette = ['#0d6efd', '#20c997', '#fd7e14', '#6f42c1', '#28a745', '#dc3545']

        const datasets = types.map((type, i) => {
          const dateMap = data[type]
          return {
            label: type,
            data: rawDates.map(date => dateMap[date] || 0),
            fill: true,
            backgroundColor: palette[i % palette.length],
            borderColor: palette[i % palette.length],
            tension: 0.3
          }
        })

        this.typeDailyChartData = {
          labels: displayLabels,
          datasets
        }
      }





  },
  mounted() {
    this.refreshMISCount();
    this.fetchMonthlyChart();
    this.fetchResourceChart(this.selectedMonth);
    this.fetchTypeDailyChart(this.selectedMonth)
  },
  watch: {
    selectedMonth(newMonth){
      this.fetchResourceChart(newMonth)
      this.fetchTypeDailyChart(newMonth)
    }
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
  padding: 0 20px;
}




.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}



.chart-container {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  justify-content: flex-start;
  margin-bottom: 40px;
}


.chart-box {
  flex: 1 1 500px;         /* Wider base width */
  max-width: 600px;        /* Cap the width */
  height: 240px;           /* Slightly taller to fit labels */
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  padding: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chart-box canvas {
  max-height: 180px;
  width: 100% !important;
  height: auto !important;
}


.month-selector {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 1rem;
}

.month-selector select {
  padding: 6px 12px;
  border-radius: 4px;
  border: 1px solid #ccc;
}



@media (max-width: 768px) {
  .dashboard-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

</style>