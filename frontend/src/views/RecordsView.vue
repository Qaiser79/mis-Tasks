<template>
    <div class="records-page">
      <h1>MIS Records</h1>
      <p>Browse all MIS entries with pagination and filters.</p>


      <section class="table-section">
      <div class="table-header">
        <h2 class="section-title">MIS Records</h2>
        <div class="tooltip-container">
          <button class="create-btn" @click="openCreateForm">
            <i class="fas fa-plus-circle"></i> Create New MIS Record
          </button>
          <span class="tooltip-text">Create new MIS record</span>
        </div>
      </div>
      <div class="search-bar">
        <input
            type="text"
            v-model="searchQuery"
            placeholder="Search by MIS No, Type, Department..."
        />
      </div>
      <div class="filters">
            <label>
                Status:
                <select v-model="selectedStatus">
                <option value="">All</option>
                <option>Completed</option>
                <option>Pending</option>
                <option>In Progress</option>
                <option>UAT-ITG</option>
                <option>UAT-USER</option>
                <option>Cancelled</option>
                </select>
            </label>

            <label>
                Resource:
                <select v-model="selectedResource">
                <option value="">All</option>
                <option v-for="team in resources" :key="team.id" :value="team.id">
                    {{ team.name }}
                </option>
                </select>
            </label>
      </div>
      <MISTable
        ref="misTableRef"
        :currentPage= "currentPage"
        :pageSize="pageSize"
        :misList="filteredList"
        paginated
        @edit-requested="startEdit"
        @delete-requested="deleteMISRecord"
      />
      <div class="pagination-controls">
        <button @click="prevPage" :disabled="currentPage === 1">Previous</button>
            <span>Page {{ currentPage }}</span>
        <button @click="nextPage" :disabled="currentPage >= totalPages">Next</button>
      </div>
      <MISForm
        :editMode="editMode"
        :editRecord="editRecord"
        :visible="showForm"
        @mis-updated="submitUpdate"
        @mis-submitted="handleCreate"
        @close="handleCloseForm"
      />
      </section>
    </div>
  </template>
  
  <script>
  import MISTable from '../components/MISTable.vue'
  import MISForm from '../components/MISForm.vue'
  import axios from 'axios'

  export default {
    components: { MISTable, MISForm },
    data() {
      return {
        records: [],
        resources: [],
        selectedStatus: '',
        selectedResource: '',
        misList: [],
        editMode: false,
        editRecord: null,
        showForm: false,
        currentPage: 1,
        pageSize: 10,
        searchQuery: ''
      }
    },
    mounted() {
        this.fetchMISRecords()
        this.fetchResources()
    },
    methods: {
        startEdit(record){
        this.editMode=true
        this.editRecord = {...record}
        this.showForm = true 
    },

    async fetchMISRecords() {
        try {
        const res = await axios.get('http://127.0.0.1:8000/mis/all')
        this.misList = Array.isArray(res.data) ? res.data : res.data.records || []
        } catch (error) {
            console.error('Failed to fetch MIS records:', error)
            this.misList = [] 
        }
    },

    async submitUpdate(updatedData){
      await axios.put(`http://127.0.0.1:8000/mis/update/${updatedData.mis_no}`, updatedData)
      this.editMode=false
      this.editRecord=null
      this.showForm = false
      await this.fetchMISRecords()
      /*this.refreshMISCount()*/
    },

    async handleCreate() {
        this.showForm = false
        this.currentPage = 1
        await this.fetchMISRecords()
    },

    async deleteMISRecord (mis_no){
      const confirmed = confirm(`Are you sure you want to delete MIS ${mis_no}?`)
      if (!confirmed) return

      try {
        await axios.delete(`http://127.0.0.1:8000/mis/delete/${mis_no}`)
        /*this.refreshMISCount()*/
        await this.fetchMISRecords()
        const maxPage = Math.ceil(this.misList.length / this.pageSize)
        if (this.currentPage > maxPage) {
            this.currentPage = Math.max(1, maxPage)
        }
      } catch (error) {
          console.error('Delete failed:', error)
          alert('Failed to delete record.')
                      }
    },
    openCreateForm() {
        this.editMode = false
        this.editRecord = null
        this.showForm = true
    },
    nextPage(){
        this.currentPage++
    },
    prevPage(){
        if (this.currentPage>1) this.currentPage--
    },
    handleCloseForm() {
        this.showForm = false
        this.editRecord = null
    },
    async fetchResources() {
        const res = await axios.get('http://127.0.0.1:8000/resources')
        this.resources = res.data
    }

    },
    computed: {
        totalPages() {
            return Math.ceil(this.filteredList.length / this.pageSize)
            },
            filteredList() {
                const query = this.searchQuery.toLowerCase()

                return this.misList.filter(record => {
                    const matchesSearch =
                    record.mis_no?.toString().includes(query) ||
                    record.mis_type?.toLowerCase().includes(query) ||
                    record.department?.toLowerCase().includes(query)

                    const matchesStatus =
                    this.selectedStatus === '' || record.mis_status === this.selectedStatus

                    const matchesResource =
                    this.selectedResource === '' || record.resource === this.selectedResource

                return matchesSearch && matchesStatus && matchesResource
            })
            }    
    }
  }
  </script>
 <style scoped>
.table-section {
  margin-bottom: 40px;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.section-title {
  font-size: 1.4rem;
  margin-bottom: 16px;
  color: #343a40;
}

.tooltip-container {
  position: relative;
  display: inline-block;
  margin: 20px 0;
}

.tooltip-container:hover .tooltip-text {
  visibility: visible;
  opacity: 1;
}

.create-btn:hover {
  background-color: #218838;
}

.create-btn {
  background-color: #28a745;
  color: white;
  padding: 10px 16px;
  font-size: 1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  margin: 20px 0;
  transition: background-color 0.2s ease;
}

.tooltip-text {
  visibility: hidden;
  width: 160px;
  background-color: #333;
  color: #fff;
  text-align: center;
  padding: 6px 10px;
  border-radius: 6px;
  position: absolute;
  z-index: 1;
  bottom: 125%; /* above the button */
  left: 50%;
  transform: translateX(-50%);
  opacity: 0;
  transition: opacity 0.3s ease;
  font-size: 0.85rem;
}

.pagination-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin-top: 20px;
}

.pagination-controls button {
  padding: 8px 16px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.pagination-controls button:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}

.search-bar {
  margin-bottom: 20px;
  text-align: left;
}

.search-bar input {
  padding: 8px 12px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 6px;
  width: 300px;
}


.filters {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
  align-items: center;
  flex-wrap: wrap;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.filters label {
  display: flex;
  flex-direction: column;
  font-weight: 600;
  color: #333;
}

.filters select {
  padding: 8px 12px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 6px;
  background-color: #fff;
  transition: border-color 0.2s ease;
  min-width: 180px;
}

.filters select:focus {
  border-color: #007bff;
  outline: none;
}

</style>