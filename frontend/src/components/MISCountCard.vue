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
  width: 100%;
  height: 160px;
  box-sizing: border-box; /* ✅ Prevents padding from breaking layout */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 16px;
  margin: 0;               /* ✅ Ensures no extra spacing conflicts */
  border-radius: 8px;
  color: #fff;
  font-weight: bold;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.card:hover {
  transform: translateY(-4px);
}

.icon {
  font-size: 1.6rem;
  margin-bottom: 8px;
}

.content h3 {
  font-size: 1rem;
  margin-bottom: 4px;
}

.content p {
  font-size: 1.2rem;
  margin: 0;
  font-weight: bold;
}

/* Color themes */
.blue-card { background-color: #007bff; }
.green-card { background-color: #28a745; }
.orange-card { background-color: #fd7e14; }
.red-card { background-color: #dc3545; }
</style>

  