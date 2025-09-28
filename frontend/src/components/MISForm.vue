<template>
    <div v-if="visible" class="modal-overlay">
        <div class="modal-content">
            <button class="close-btn" @click="$emit('close')">
                <i class="fas fa-times"></i>
            </button>

            <form @submit.prevent="submitForm" class="mis-form">
                <h3>{{ editMode ? 'Edit MIS Record' : 'Create MIS Record' }}</h3>
            
                <div class="form-row">
                    <label for="mis_no">MIS No</label>
                    <input id="mis_no" v-model="form.mis_no" type="number" />
                </div>
            
                <div class="form-row">
                    <label for="mis_type">MIS Type</label>
                    <input id="mis_type" v-model="form.mis_type" type="text" />
                </div>
            
                <div class="form-row">
                    <label for="department">Department</label>
                    <input id="department" v-model="form.department" type="text" />
                </div>
            
                <div class="form-row">
                    <label for="arrival_date">Arrival Date</label>
                    <input id="arrival_date" v-model="form.arrival_date" type="date" />
                </div>
            
                <div class="form-row">
                    <label for="last_uat_date">Last UAT Date</label>
                    <input id="last_uat_date" v-model="form.last_uat_date" type="date" />
                </div>
            
                <div class="form-row">
                    <label for="mis_description">MIS Description</label>
                    <textarea id="mis_description" v-model="form.mis_description"></textarea>
                </div>
            
                <div class="form-row">
                    <label for="mis_status">MIS Status</label>
                    <select id="mis_status" v-model="form.mis_status">
                    <option value="">Select Status</option>
                    <option>Completed</option>
                    <option>Pending</option>
                    <option>In Progress</option>
                    <option>UAT-ITG</option>
                    <option>UAT-USER</option>
                    <option>Cancelled</option>
                    </select>
                </div>
            
                <div class="form-row">
                    <label for="comment">Comment</label>
                    <textarea id="comment" v-model="form.comment"></textarea>
                </div>
            
                <div class="form-row">
                    <label for="completed_date">Completed Date</label>
                    <input id="completed_date" v-model="form.completed_date" type="date" />
                </div>
            
                <div class="form-row">
                    <label for="assigned_date">Assigned Date</label>
                    <input id="assigned_date" v-model="form.assigned_date" type="date" />
                </div>
            
                <div class="form-row">
                    <label for="target_date">Target Date</label>
                    <input id="target_date" v-model="form.target_date" type="date" />
                </div>
            
                <div class="form-row">
                    <label for="resource">Resource</label>
                        <select id="resource" v-model="form.resource">
                            <option value="">Select Resource</option>
                            <option v-for="team in resources" :key="team.id" :value="team.id">
                                {{ team.name }}
                            </option>
                        </select>
                </div>
            
                <button type="submit">Submit</button>
                <p v-if="message">{{ message }}</p>
            </form>
        </div>
    </div>
  </template>
  
  

<script>
    import axios from 'axios'

    export default{
        name: 'MISForm',
        data(){
            return {
                form: {
                    mis_no: null,
                    mis_type: '',
                    department: '',
                    arrival_date: '',
                    last_uat_date: '',
                    mis_description: '',
                    mis_status: '',
                    comment: '',
                    completed_date: '',
                    assigned_date: '',
                    target_date: '',
                    resource: null
                },
                resources: [],
                message: ''
            }
        },
        methods: {
            submitForm() {
                console.log("Form submitted")

                if (this.editMode) {
                    this.$emit('mis-updated', this.form)  // send full form data to App.vue
                } else {
                    axios.post('http://127.0.0.1:8000/mis', this.form)
                    .then(response => {
                        this.message = response.data.message || 'Success'
                        this.$emit('mis-submitted')
                        this.resetForm()
                    })
                    .catch(error => {
                        console.error('Error:', error)
                        this.message = 'Failed to create MIS record.'
                    })
                }
                },
            resetForm() {
                this.form={
                        mis_no: null,
                        mis_type: '',
                        department: '',
                        arrival_date: '',
                        last_uat_date: '',
                        mis_description: '',
                        mis_status: '',
                        comment: '',
                        completed_date: '',
                        assigned_date: '',
                        target_date: '',
                        resource: null
                    }
            },
            fetchResources() {
                    axios.get('http://127.0.0.1:8000/resources')
                    .then(res => {
                        this.resources = res.data
                    })
                    .catch(err => {
                        console.error('Failed to load resources:', err)
                    })
            },
        },
        mounted() {
            this.fetchResources()
        },

        props:{
            editMode: Boolean,
            editRecord: Object,
            visible: Boolean
        },
        watch: {
            editMode: {
                handler(val) {
                if (!val && this.visible) {
                    this.resetForm()
                }
                },
                immediate: true
            },
            editRecord: {
                handler(newVal) {
                if (newVal && this.editMode) {
                    this.form = { ...newVal }
                }
                },
                immediate: true
            }
            }
}
</script>

<style scoped>
.mis-form {
  max-width: 600px;
  margin: 30px auto;
  padding: 24px;
  background-color: #f8f9fa;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.mis-form h3 {
  text-align: center;
  margin-bottom: 20px;
  font-size: 1.4rem;
  color: #333;
}

.form-row {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
}

.form-row label {
  width: 160px;
  font-weight: 600;
  margin-right: 12px;
  color: #333;
}

.form-row input,
.form-row select,
.form-row textarea {
  flex: 1;
  padding: 10px 12px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 6px;
  transition: border-color 0.2s ease;
}

.form-row textarea {
  resize: vertical;
  min-height: 60px;
}

.form-row input:focus,
.form-row select:focus,
.form-row textarea:focus {
  border-color: #007bff;
  outline: none;
}

.mis-form button {
  background-color: #007bff;
  color: white;
  padding: 10px 16px;
  font-size: 1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s ease;
  width: 100%;
  margin-top: 20px;
}

.mis-form button:hover {
  background-color: #0056b3;
}

.mis-form p {
  margin-top: 12px;
  text-align: center;
  font-weight: 500;
  color: #28a745;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background-color: #fff;
  position: relative;
  border-radius: 12px;
  padding: 30px;
  width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 8px 24px rgba(0,0,0,0.2);
}

.close-btn {
  position: absolute;
  top: 16px;
  right: 20px;
  background: none;
  border: none;
  font-size: 1.4rem;
  color: #666;
  cursor: pointer;
  z-index: 10;
}

.close-btn:hover {
  color: #000;
}


</style>

