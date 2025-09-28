<template>
    <aside class="sidebar">
      <h2>MIS Panel</h2>
        <ul class="nav-list">
            <li>
              <router-link to="/" class="nav-item">
                <i class="fas fa-home"></i> Dashboard
              </router-link>
            </li>
            <li @click="$emit('create-requested')">
              <i class="fas fa-plus-circle"></i> Create Record
            </li>
            <li>
              <router-link to="/records" class="nav-item">
                <i class="fas fa-table"></i> View Records
              </router-link>
            </li>
            <li>
              <i class="fas fa-chart-bar"></i> Summary
            </li>
            <li>
              <i class="fas fa-cog"></i> Settings
            </li>
        </ul>

    </aside>
  </template>
  
  <script>
  export default {
    name: 'Sidebar'
  }
  </script>
  
  <style scoped>
  .sidebar {
    width: 220px;
    background-color: #343a40;
    color: white;
    padding: 20px;
    font-family: 'Segoe UI', sans-serif;
  }
  
  .sidebar h2 {
    font-size: 1.2rem;
    margin-bottom: 20px;
    color: #f8f9fa;
  }
  
  .nav-list {
    list-style: none;
    padding: 0;
  }
  
  .nav-list li {
    margin-bottom: 16px;
    cursor: pointer;
    font-size: 1rem;
    display: flex;
    align-items: center;
    gap: 10px;
    transition: color 0.2s ease;
  }
  
  .nav-list li:hover {
    color: #20c997;
  }

  .nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  color: white;
  text-decoration: none;
  font-size: 1rem;
  transition: color 0.2s ease;
}

.nav-item:hover {
  color: #20c997;
}

.router-link-active {
  font-weight: bold;
  color: #20c997;
}

  </style>
  