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

  </div>
</template>
<script>
  import axios from 'axios'
  import MISCountCard from '../components/MISCountCard.vue'
  /*import Sidebar from '../components/Sidebar.vue'*/
  export default {
    components: { MISCountCard},
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
      console.log('Updated statusCounts:', this.statusCounts)
    }



  },
  mounted() {
    this.refreshMISCount()
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

</style>