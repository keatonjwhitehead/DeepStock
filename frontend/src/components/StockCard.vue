<template>
  <div :class = "custom">
    <fusioncharts
    :type="type"
    :width="width"
    :height="height"
    :dataFormat="dataFormat"
    :dataSource="dataSource"
    ></fusioncharts>

  </div>
</template>
<script>
import { mapGetters } from 'vuex';
export default {
  name: 'stock-card',
  props: {
    custom: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      type: "timeseries",
      width: "100%",
      height: "100%",
      dataFormat: "json",
      dataStore: new FusionCharts.DataStore(),
      schema: [{
        name: "Time",
        type: "date",
        format: "%Y-%m-%d %-H:%M:%S"
      }, {
        name: "Price",
        type: "number"
      }],
    }
  },
  computed:{
    dataSource(){
      this.dataStore.dispose()
      this.dataStore = new FusionCharts.DataStore()
      return ({
        chart: {theme: "candy"},
        navigator: {
          enabled: 0
        },
        caption: {
           text: "Intraday movements of " + this.ticker
        },
        yaxis: [
          {
            plot: [
              {
                value: "Price",
                //type: 'line',
                connectnulldata: true,
                style: {
                  "plot.null": {
                    "stroke-dasharray": "none",
                  }
                }
              }
            ]
          }
        ],
        //numbersuffix: "K",
        theme: "candy",
        data: this.dataStore.createDataTable(this.chartData, this.schema)
      })
    },
    ...mapGetters({
      ticker:'getTicker',
      chartData: 'getChartData'
    })
  },
}
</script>
