<template>
<div class="page-container">

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

    <section class="chart-section">
      <div class="title-selector-container">
        <h2 class="section-title">MIS Analytics</h2>
          <div class="month-selector-wrapper">
            <div class="month-selector">
                <label for="month">Select Month:</label>
                  <select id="month" v-model="selectedMonth" >
                    <option v-for="(name, index) in monthNames" :key="index" :value="index + 1">
                      {{ name }}
                    </option>
                  </select>
            </div>
          </div>
      </div>

    <div class="chart-grid">
      <div class="chart-box">
        <StatusChart
            v-if="chartData.datasets[0].data.length > 0"
            :data="chartData"
            :options="chartOptions"
        />
        <div v-else class="chart-placeholder">No data available</div>
        </div>

        <div class="chart-box">
        <MonthlyChart 
        v-if="monthlyChartData.datasets[0].data.length > 0"
        :data="monthlyChartData"
        :options="monthlyChartOptions"
        />
        <div v-else class="chart-placeholder">No data available</div>
      </div>


        <div class="chart-box">
          <MonthlyChart
            v-if="resourceChartData.datasets[0].data.length > 0"
            :data="resourceChartData"
            :options="resourceChartOptions"
          />
          <div v-else class="chart-placeholder">No data available</div>
      </div>

        <div class="chart-box">
          <TypeDailyChart
            v-if="typeDailyChartData.datasets.length > 0"
            :data="typeDailyChartData"
            :options="typeDailyChartOptions"
          />
          <div v-else class="chart-placeholder">No data available</div>
        </div>

      
    </div>
</section>

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
            maintainAspectRatio: false,
            layout: {
              padding: 10 // Add padding to prevent clipping
            },
                plugins: {
                    legend: {
                      position: 'right',
                      labels: {
                          boxWidth: 20, // Smaller legend boxes
                          font: { size: 10 }, // Smaller legend text
                          padding: 10
                      }

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

        resourceChartOptions: {
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

```vue
<style scoped>
.page-container {
  max-width: 90vw;
  margin: 0 auto;
  padding: 10px;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #1e293b; /* slate-800 */
color: #f1f5f9; /* slate-100 */
}



.section-title {
  font-size: 1.125rem;
  font-weight: 600;
  margin-bottom: 0;
  color: #ffffff;
}

.card-section {
  margin-bottom: 12px;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 10px;
  max-width: 100%;
  margin: 0 auto;
}

.card-placeholder {
  grid-column: span 4;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100px;
  background-color: #f3f4f6;
  color: #6b7280;
  font-size: 0.75rem;
  border-radius: 6px;
}

.chart-section {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.title-selector-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  margin-bottom: 12px;
}

.month-selector-wrapper {
  position: absolute;
  left: 50%;
  transform: translateX(-50%); /* Center in full container width */
  display: flex;
  justify-content: center;
  width: auto; /* Fit content */
}

.month-selector {
  display: flex;
  align-items: center;
  gap: 12px;
  padding-left: 180px; /* Prevent overlap with section-title (~120px for "MIS Analytics") */
}

.month-selector label {
  font-size: 1.125rem;
  font-weight: 600;
  color: #ffffff;
}

.month-selector select {
  padding: 8px 16px;
  border-radius: 6px;
  border: 2px solid #d1d5db;
  background-color: #ffffff;
  font-size: 1.125rem;
  font-weight: 500;
  color: #1a202c;
  cursor: pointer;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
  min-width: 250px;
  appearance: none;
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12"><path fill="#1a202c" d="M2 4l4 4 4-4H2z"/></svg>');
  background-repeat: no-repeat;
  background-position: right 16px center;
}

.month-selector select:hover {
  border-color: #3b82f6;
}

.month-selector select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
}

.chart-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(600px, 1fr));
  gap: 12px;
  max-width: 100%;
  margin: 0;
}

.chart-box {
  background-color: #fff;
  border-radius: 6px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  padding: 10px;
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chart-box canvas {
  max-width: 100%;
  max-height: 250px;
  background-color: #f9fafb; /* light gray */
}

.chart-box:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
}

.chart-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #6b7280;
  font-size: 0.75rem;
  font-weight: 500;
}
.chart-box {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

@media (max-width: 1280px) {
  .page-container {
    max-width: 95vw;
  }
  .dashboard-grid, .chart-grid, .title-selector-container {
    max-width: 100%;
  }
  .card-placeholder {
    grid-column: span 2;
  }
}

@media (max-width: 768px) {
  .title-selector-container {
    position: static; /* Disable absolute positioning */
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  .month-selector-wrapper {
    position: static; /* Normal flow */
    transform: none;
    width: 100%;
  }
  .month-selector {
    padding-left: 0; /* Remove padding */
    width: 100%;
  }
  .month-selector select {
    min-width: 200px;
  }
}

@media (max-width: 480px) {
  .page-container {
    padding: 8px;
  }
  .dashboard-header h1 {
    font-size: 1.25rem;
  }
  .section-title {
    font-size: 1rem;
  }
  .month-selector label, .month-selector select {
    font-size: 0.875rem;
  }
  .month-selector select {
    padding: 6px 12px;
    min-width: 100%;
  }
}
</style>