<template>
<div :class = "custom">
  <b>Sentiment Forecast:</b>
  <p style="color:white">{{pred}}</p>

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

import {mapGetters} from 'vuex';

export default {
  name: "sentiment-card",
  props: {
    custom: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      type: "column2d",
      width: "100%",
      height: "100%",
      dataFormat: "json",
    }
  },
  computed:{
    test(){
      console.log(this.sent)
    },
    dataSource(){
      // this.dataStore.dispose()
      // this.dataStore = new FusionCharts.DataStore()
      return ({
        chart: {
          caption: "7 Day Twitter Sentiment of " + this.ticker,
          //subcaption: "In MMbbl = One Million barrels",
          xaxisname: "Day",
          yaxisname: "Company",
          numbersuffix: "%",
          valueFontSize: "10",
          theme: "candy"
        },
        navigator: {
          enabled: 0
        },
        caption: {
           text: "Tweet Sentiment of " + this.ticker
        },
        yaxis: [
          {
            plot: [
              {
                value: "Sentiment",
                //type: 'line',
                connectnulldata: true,
              }
            ]
          }
        ],
        //numbersuffix: "K",
        theme: "candy",

        data: this.sent.map((s, i) => {return {label: i, value: s}})
      })
    },
    ...mapGetters({
      ticker:'getTicker',
      sent: 'getTweetSent',
      pred: 'getPrediction'
    })
  },
};



</script>
