<template>
<div>
  <div>
    <GmapMap
      :center="{lat:24.8534721, lng:121.3490477}"
      :zoom="15"
      style="width: auto; height: 450px"
      >
	  <GmapInfoWindow :options="infoOptions" :position="infoWindowPos" :opened="infoWinOpen" @closeclick="infoWinOpen=false" >
		<span v-html="infoContent"></span>
	  </GmapInfoWindow>
      <GmapMarker
        :key="index"
        v-for="(m, index) in marker_filters"
        :position="m.position"
        :clickable="true"
        :draggable="true"
        @click="center=m.position;toggleInfoWindow(m,index)"
      />
    </GmapMap>
  </div>
  <b-container style="padding-top: 20px; padding-bottom: 20px">
	<b-row>
	  <b-col>
		<b-card border-variant="primary" header-bg-variant="primary" header-text-variant="white" header="事故日期區間" align="center">
		  <datepicker wrapper-class="picker-wrapper" v-model="fromDate"></datepicker>
		  <datepicker wrapper-class="picker-wrapper" v-model="toDate"></datepicker>
		</b-card>
	  </b-col>
	  <b-col>
		<b-card border-variant="primary" header-bg-variant="primary" header-text-variant="white" header="事故時間區間" align="center">
		  <input v-model="fromTime" type="time"></input>
		  <input v-model="toTime" type="time"></input>
		</b-card>
	  </b-col>
	</b-row>
	<b-row>
	  <b-col>
		<b-card border-variant="primary" header-bg-variant="primary" header-text-variant="white" header="事故選擇" align="center">
		  <b-form-group label="事故參與方">
			<b-form-checkbox v-model="self_contributing">自摔/自撞</b-form-checkbox>
			<b-form-checkbox v-model="multiple_contributing">涉入第三人</b-form-checkbox>
		  </b-form-group>
		  <b-form-group label="涉入車種">
			<b-form-checkbox v-model="normal_motorcycle">普通重型機車</b-form-checkbox>
			<b-form-checkbox v-model="big_motorcycle">大型重型機車</b-form-checkbox>
			<b-form-checkbox v-model="light_motorcycle">輕型機車</b-form-checkbox>
			<b-form-checkbox v-model="car">小客車</b-form-checkbox>
		  </b-form-group>
		</b-card>
	  </b-col>
	</b-row>
	<b-row>
	  <b-col>
		<b-card border-variant="danger" header-bg-variant="danger" header-text-variant="white" header="總事故件數" align="center">
		  {{ marker_filters.length }} 件
		</b-card>
	  </b-col>
	</b-row>
	<b-row>
	  <b-col>
		<b-card border-variant="danger" header-bg-variant="danger" header-text-variant="white" header="事故時間軸" align="center">
		  <highcharts :options="timelineChartOptions"></highcharts>
		</b-card>
	  </b-col>
	</b-row>
  </b-container>
</div>
</template>

<script>
  import Datepicker from 'vuejs-datepicker'
  import moment from "moment"
  import { extendMoment } from 'moment-range'

  function minutesOfTime(m) {
    return parseInt(m.split(':')[0]) * 60 + parseInt(m.split(':')[1])
  }

export default {
  name: 'HelloWorld',
  components: {
	Datepicker
  },
  data() {
    return {
	  moment: extendMoment(moment),
	  infoContent: '',
	  infoWindowPos: null,
	  infoWinOpen: false,
	  infoOptions: {
		pixelOffset: {
		  width: 0,
		  height: -35
		}
	  },
	  currentMidx: null,
	  timelineChartOptions: {},

	  // Date picker
	  fromDate: moment(this.$route.query.from ? this.$route.query.from : '2014-1-1').toDate(),
	  toDate: moment(this.$route.query.to ? this.$route.query.to : '2017-12-31').toDate(),

	  // Times
	  fromTime: "00:00",
	  toTime: "23:59",

	  // Filters
	  self_contributing: this.$route.query.sc === "1" ? true : false,
	  multiple_contributing: this.$route.query.mc === "1" ? true : false,
	  normal_motorcycle: this.$route.query.iv && this.$route.query.iv.indexOf('nm') > -1 ? true : false,
	  big_motorcycle: this.$route.query.iv && this.$route.query.iv.indexOf('bm') > -1 ? true : false,
	  light_motorcycle: this.$route.query.iv && this.$route.query.iv.indexOf('lm') > -1 ? true : false,
	  car: this.$route.query.iv && this.$route.query.iv.indexOf('car') > -1 ? true : false,
	  markers: [],
	  marker_filters: []
    }
  },
  watch: {
	fromDate: function(val) {
	  this.updateFilterMarkers()
	},
	toDate: function(val) {
	  this.updateFilterMarkers()
	},
	fromTime: function(val) {
	  this.updateFilterMarkers()
	},
	toTime: function(val) {
	  this.updateFilterMarkers()
	},
	self_contributing: function(val) {
	  this.updateFilterMarkers()
	},
	multiple_contributing: function(val) {
	  this.updateFilterMarkers()
	},
	normal_motorcycle: function(val) {
	  this.updateFilterMarkers()
	},
	big_motorcycle: function(val) {
	  this.updateFilterMarkers()
	},
	light_motorcycle: function(val) {
	  this.updateFilterMarkers()
	},
	car: function(val) {
	  this.updateFilterMarkers()
	}
  },
  methods: {
	toggleInfoWindow: function(marker, idx) {
	  this.infoWindowPos = marker.position
	  this.infoContent = marker.description.replace(/\n/g, "<br />");

	  if (this.currentMidx == idx) {
		this.infoWinOpen = !this.infoWinOpen
	  } else {
		this.currentMidx = idx
		this.infoWinOpen = true
	  }
	},
    updateFilterMarkers: function () {
	  this.marker_filters = []
	  var startTime = minutesOfTime(this.fromTime)
	  var endTime = minutesOfTime(this.toTime)
      for (var i = 0; i < this.markers.length; ++i) {
		var token = true
		var incident = this.markers[i]

		// Date
		var dateRange = this.moment().range(this.fromDate, this.toDate)
		if (!dateRange.contains(moment(incident.date, "YYYY-MM-DD").toDate())) {
		  token = false
		}

		// Time
		if (incident.minutes > endTime || incident.minutes < startTime) {
		  token = false
		}

		// Contributing
		if (this.self_contributing === false && this.multiple_contributing === false) {
		  token = false
		} else if (this.self_contributing === true && this.multiple_contributing === false) {
		  if (incident.contributing.length != 1) {
			token = false
		  }
		} else if (this.self_contributing === false && this.multiple_contributing === true) {
		  if (incident.contributing.length == 1) {
			token = false
		  }
		}

		// Involved vehicle type
		if (this.normal_motorcycle === true) {
		  if (incident.involve_normal_motorcycle === false) {
			token = false
		  }
		}
		if (this.big_motorcycle === true) {
		  if (incident.involve_big_motorcycle === false) {
			token = false
		  }
		}
		if (this.light_motorcycle === true) {
		  if (incident.involve_light_motorcycle === false) {
			token = false
		  }
		}
		if (this.car === true) {
		  if (incident.involve_car === false) {
			token = false
		  }
		}

		if (token === true) {
		  this.marker_filters.push(this.markers[i])
		}
      }
	  this.updateTimelineChart()
    },
	updateTimelineChart: function() {
	  var data = []
	  var dd = new Proxy({}, {
		get: (target, name) => name in target ? target[name] : 0
	  })

	  var start = this.fromDate
	  var end = this.toDate

	  // Convert to date
	  for (var i = 0; i < this.marker_filters.length; ++i) {
		dd[this.marker_filters[i].date] += 1
	  }

	  console.log(dd)
	  // Push into data
	  for (var m = moment(start); m.isBefore(end); m.add(1, 'days')) {
		data.push([m.toDate(), dd[m.format('YYYY-MM-DD')]])
	  }

	  this.timelineChartOptions = {
		chart: {
		  type: 'column',
		  polar: true,
		  height: 200
		},
		xAxis: {
		  type: 'datetime',
		},
		yAxis: {
		  tickInterval: 1
		},
		title: {
		  text: ''
		},
		series: [{
		  name: '台7乙事故數量',
		  data: data
		}]
	  }
	}
  },
  mounted () {
	console.log(this.$route.query)
    this.axios
      .get('https://t7b.freeway.pw/api/incidents')
      .then(response => (
        this.markers = response.data.data,
		this.updateFilterMarkers(),
		this.updateTimelineChart()
      ))
  }

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}

.picker-wrapper {
	display: inline-block;
}

.container > .row {
	padding-top: 5px;
	padding-bottom: 5px;
}

</style>
