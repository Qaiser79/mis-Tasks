<template>
  <div class="main-layout">
    <Sidebar />
    <div class="content-area">
      <router-view />
    </div>
  </div>
</template>

<script>
import Sidebar from './components/Sidebar.vue'

export default {
  components: { Sidebar }
}
</script>

<style scoped>
.main-layout {
  display: flex;
  min-height: 100vh;
}

.content-area {
  flex: 1;
  padding: 30px 40px;
  background-color: #f8f9fa;
}
</style>
