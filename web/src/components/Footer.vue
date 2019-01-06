<template>
  <footer class="main-footer">
    <div class="main-footer-container">
      <div class="main-footer-content">
        <a href="/">台7乙交通事故互動地圖</a>
		<a href="https://www.npa.gov.tw/NPAGip/wSite/lp?ctNode=12854&CtUnit=2633&BaseDSD=7&mp=3">原始資料來源</a>
		<a href="https://github.com/mlouielu/t7b-incident">GitHub</a>
		<a href="https://drive.google.com/open?id=1dQJedHZMkBw3LE9kHxW5quamcjjdv2uz&usp=sharing">Google Maps</a>
      </div>
    </div>
  </footer>
</template>
<script>
export default {
  props: {
    title: {
      type: String,
      required: true
    }
  },
  data(){
      return{
      }
  }
}
</script>
<style scoped>
.main-footer {
  background-color: #90CAF9;
  height: 152px;
  flex: 1 0 auto;
  padding: 0 16px;
}

.main-footer-container {
  display: -webkit-box;
  display: flex;
  height: 100%;
  max-width: 100%;
  align-items: center;
  -webkit-box-pack: justify;
  justify-content: space-between;
  transition: .3s cubic-bezier(.4,0,.2,1);
  transition-property: max-width;
}

.main-footer-content {
}

.main-footer-content a {
  color: #000 !important;
  padding-left: 16px;
}
</style>
