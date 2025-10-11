<template>
    <div class="editor-dashboard">
      <h2 v-if="currentUser">Welcome,{{ currentUser.team_id }}</h2>
      <h2 v-else>Welcome</h2>
      <div class="card-grid">
        <MISCountCard
          v-for="card in cards"
          :key="card.title"
          :title="card.title"
          :count="card.count"
          :bgColor="card.bgColor"
          :iconClass="card.iconClass"
        />
      </div>
      <MISSummaryTable v-if="recentMIS && recentMIS.length" :records="recentMIS" />
      <MISProgressBar :breakdown="statusBreakdown" />
    </div>
</template>

<script>

import MISCountCard
 from '../components/MISCountCard.vue'
import MISSummaryTable from '../components/MISSummaryTable.vue'
import MISProgressBar from '../components/MISProgressBar.vue'
 import axios from 'axios'

 export default{
    components: { MISCountCard, MISSummaryTable , MISProgressBar },
    data(){
        return {
            currentUser: JSON.parse(localStorage.getItem('currentUser')) || {},
            cards: [],
            recentMIS: [],
            statusBreakdown: {}
        }
    },
    async mounted(){
        const statuses = [
            { title: 'Completed', color: '#28a745', icon: 'fas fa-check-circle' },
            { title: 'Pending', color: '#fd7e14', icon: 'fas fa-hourglass-half' },
            { title: 'In Progress', color: '#17a2b8', icon: 'fas fa-spinner' },
            { title: 'Cancelled', color: '#dc3545', icon: 'fas fa-times-circle' }
            ]
        const teamId= this.currentUser.team_id
        const promises= statuses.map(async s => {
        const res = await axios.get('http://127.0.0.1:8000/mis/status-count',{
        params: { status: s.title, team_id: teamId }
        })

        return {
            title: s.title,
            count: Number(res.data.count) || 0,
            bgColor: s.color,
            iconClass: s.icon
        }

        })
        this.cards = await Promise.all(promises)
        const res1 = await axios.get(`http://127.0.0.1:8000/mis/recent/${teamId}`)
        this.recentMIS = res1.data.records
        const breakdown = {}
        for (const s of statuses) {
            const res = await axios.get('http://127.0.0.1:8000/mis/status-count', {
              params: { status: s.title, team_id: teamId }
            })
            breakdown[s.title] = Number(res.data.count) || 0
          }
          this.statusBreakdown = breakdown
          console.log('Status Breakdown:', this.statusBreakdown)
    }
    
 }

</script>

<style scoped>
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1rem;
  margin-top: 1.5rem;
}
</style>