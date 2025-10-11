<template>
    <div class="progress-widget">
      <h3>Status Breakdown</h3>
      <div class="bar">
        <div
          v-for="(value, status) in breakdown"
          :key="status"
          class="segment"
          :style="{ width: getWidth(value) + '%', backgroundColor: getColor(status) }"
          :title="`${status}: ${value}`"
        ></div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'MISProgressBar',
    props: {
      breakdown: { type: Object, required: true }
    },
    computed: {
      total() {
        return Object.values(this.breakdown).reduce((a, b) => a + b, 0)
      }
    },
    methods: {
      getWidth(value) {
        return this.total ? (value / this.total) * 100 : 0
      },
      getColor(status) {
        const map = {
          Completed: '#28a745',
          Pending: '#fd7e14',
          'In Progress': '#17a2b8',
          Cancelled: '#dc3545'
        }
        return map[status] || '#6c757d'
      }
    }
  }
  </script>
  
  <style scoped>
  .progress-widget {
    margin-top: 2rem;
  }
  .bar {
    display: flex;
    height: 24px;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: inset 0 1px 3px rgba(0,0,0,0.2);
  }
  .segment {
    height: 100%;
  }
  </style>
  