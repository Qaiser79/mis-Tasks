<template>
    <table class="mis-table">
    <thead>
      <tr>
        <th>MIS No</th>
        <th>Type</th>
        <th>Status</th>
        <th>Department</th>
        <th>Actions</th>
      </tr>
    </thead>
    <tbody>
        <tr v-for="record in paginatedRecords" :key="record.mis_no">
            <td>{{ record.mis_no }}</td>
            <td>{{ record.mis_type }}</td>
            <td>{{ record.mis_status }}</td>
            <td>{{ record.department }}</td>
            <td>
                <button @click="$emit('edit-requested', record)" class="action-btn edit">
                    <i class="fas fa-edit"></i> Edit
                </button>
                <button @click="$emit('delete-requested', record.mis_no)" class="action-btn delete">
                    <i class="fas fa-trash-alt"></i> Delete
                </button>
            </td>

        </tr>
    </tbody>
    </table>
</template>

<script>
export default {
  name: 'MISTable',
  props: {
    misList: {
      type: Array,
      required: true
    },
    currentPage: {
      type: Number,
      default: 1
    },
    pageSize: {
      type: Number,
      default: 10
    },
    paginated: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    paginatedRecords() {
      if (!this.paginated) return this.misList
      const start = (this.currentPage - 1) * this.pageSize
      return this.misList.slice(start, start + this.pageSize)
    }
  }
}
</script>


<style scoped>
.mis-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
}

.mis-table th {
  background-color: #f0f4f8;
  color: #333;
  text-align: left;
  padding: 12px;
  font-weight: 600;
  border-bottom: 2px solid #dee2e6;
}

.mis-table td {
  padding: 12px;
  border-bottom: 1px solid #e9ecef;
}

.mis-table tr:nth-child(even) {
  background-color: #f8f9fa;
}

.mis-table tr:hover {
  background-color: #e2e6ea;
}

.mis-table td:last-child {
  display: flex;
  gap: 10px;
}

button {
  background-color: transparent;
  border: none;
  cursor: pointer;
  font-size: 0.9rem;
  padding: 6px 10px;
  border-radius: 4px;
  transition: background-color 0.2s ease;
}

button:hover {
  background-color: #e0e0e0;
}

button:first-child {
  color: #007bff;
}

button:last-child {
  color: #dc3545;
}

.action-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 0.9rem;
  padding: 6px 10px;
  border-radius: 4px;
  transition: background-color 0.2s ease;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.action-btn:hover {
  background-color: #e0e0e0;
}

.action-btn.edit {
  color: #007bff;
}

.action-btn.delete {
  color: #dc3545;
}



</style>
