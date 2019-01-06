<template>
  <div id="app">
	<b-navbar type="dark" variant="info">
	  <b-navbar-brand href="#">台7乙交通事故互動地圖</b-navbar-brand>
	</b-navbar>
    <router-view/>
	<app-footer></app-footer>
  </div>
</template>

<script>
  import Footer from './components/Footer.vue'

export default {
  name: 'App',
  components: {
	'app-footer': Footer
  }
}
</script>
