<template>
    <div class="summary-table">
      <h3>Recent MIS Summary</h3>
      <table>
        <thead>
          <tr>
            <th>MIS ID</th>
            <th>Type</th>
            <th>Status</th>
            <th>Target Date</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="record in records" :key="record.mis_no">
            <td>{{ record.mis_no }}</td>
            <td>{{ record.mis_type }}</td>
            <td>{{ record.mis_status }}</td>
            <td>{{ formatDate(record.target_date) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script>
  export default {
    name: 'MISSummaryTable ',
    props: {
      records: { type: Array, required: true }
    },
    methods: {
      formatDate(date) {
        return new Date(date).toLocaleDateString()
      }
    }
  }
  </script>
  
  <style scoped>
  .summary-table {
    margin-top: 2rem;
    background: #fff;
    border-radius: 8px;
    padding: 1rem;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
  }
  table {
    width: 100%;
    border-collapse: collapse;
  }
  th, td {
    padding: 0.5rem;
    text-align: left;
  }
  th {
    background-color: #f8f9fa;
  }
  tr:nth-child(even) {
    background-color: #f2f2f2;
  }
  </style>
  