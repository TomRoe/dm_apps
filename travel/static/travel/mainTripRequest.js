new Vue({
  el: '#app',
  vuetify: new Vuetify(),
  data: () => ({
    alignTop: false,
    avatar: false,
    dense: false,
    fillDot: false,
    hideDot: false,
    icon: false,
    iconColor: false,
    left: false,
    reverse: false,
    right: false,
    small: false,
  }),
})



  var app = new Vue({
    el: '#app',
    delimiters: ["${", "}"],
    data: {
      loading_costs: true,
      costs: [],
    },
    methods: {
      getCosts(tripRequestId=trip_request_id) {
        this.loading_costs = true;
        let endpoint = `/api/travel/trip-request/${tripRequestId}/costs/`;
        apiService(endpoint)
            .then(response => {
              this.loading_costs = false;
              this.costs = response;

            })
      },
      openCostPopout(costId) {
        popitup(`/travel-plans/trip-request-cost/${costId}/edit/`)
      }


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
      totalCosts () {
        amountArray = []
        for (var i = 0; i < this.costs.length; i++) {
          amountArray.push(this.costs[i].amount_cad)
        }
        return amountArray.reduce((a, b) => a + b, 0)
      }
    },
    created() {
      this.getCosts()
    },
    mounted() {
    },
  });
