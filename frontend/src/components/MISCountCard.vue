<template>
    <div class="card" :style="{ backgroundColor: bgColor }">
      <div class="icon">
        <i :class="iconClass"></i>
      </div>
      <div class="content">
        <h3>{{ title }}</h3>
        <p>{{ count }}</p>
      </div>
    </div>
  </template>
  
  <script>
  
  
  export default {
    name: 'MISCountCard',
    props: {
      title:{type: String, required: true},
      count: {type: Number, required: true},
      bgColor: { type: String, default: '#007bff' },
      iconClass: { type: String, default: 'fas fa-chart-bar' }
    }

  }
  </script>
  
  <style scoped>
.card {
  display: flex;
  align-items: center;
  padding: 16px 20px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  color: white;
  width: 240px;
  margin: 10px;
  transition: transform 0.2s ease;
}

.card:hover {
  transform: translateY(-4px);
}

.icon {
  font-size: 2rem;
  margin-right: 16px;
}

.content h3 {
  margin: 0;
  font-size: 1rem;
  font-weight: 500;
}

.content p {
  margin: 4px 0 0;
  font-size: 1.6rem;
  font-weight: bold;
}

/* Color themes */
.blue-card { background-color: #007bff; }
.green-card { background-color: #28a745; }
.orange-card { background-color: #fd7e14; }
.red-card { background-color: #dc3545; }
</style>

  