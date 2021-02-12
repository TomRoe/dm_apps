var app = new Vue({
  el: '#app',
  delimiters: ["${", "}"],
  data: {
    loading_trip: true,
    loading_request: true,

    trip: {},
    request: {},
  },
  methods: {
    getRequest() {
      this.loading_costs = true;
      let endpoint = `/api/travel/requests/${tripRequestId}/`;
      apiService(endpoint)
          .then(response => {
            this.loading_request = false;
            this.request = response;
            this.getTrip(this.request.trip.id)
          })
    },
    getTrip(tripId) {
      this.loading_costs = true;
      let endpoint = `/api/travel/trips/${tripId}/`;
      apiService(endpoint)
          .then(response => {
            this.loading_trip = false;
            this.trip = response;
          })
    },
  },
  filters: {
    floatformat: function (value, precision = 2) {
      if (!value) return '';
      value = value.toFixed(precision);
      return value
    },
    zero2NullMark: function (value) {
      if (!value || value === "0.00" || value == 0) return '---';
      return value
    },
    nz: function (value, arg = "---") {
      if (value == null) return arg;
      return value
    },
    yesNo: function (value) {
      if (value == null || value == false || value == 0) return 'No';
      return "Yes"
    },
    percentage: function (value, decimals) {
      // https://gist.github.com/belsrc/672b75d1f89a9a5c192c
      if (!value) {
        value = 0;
      }

      if (!decimals) {
        decimals = 0;
      }

      value = value * 100;
      value = Math.round(value * Math.pow(10, decimals)) / Math.pow(10, decimals);
      value = value + '%';
      return value;
    }
  },
  computed: {

  },
  created() {
    this.getRequest()
  },
  mounted() {
  },
});
