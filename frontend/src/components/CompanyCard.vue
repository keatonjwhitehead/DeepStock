<template>
  <div :class = "custom">
    <h3 class="card-header">About </h3>
    <b-row class="">
      <div class = " list-group list-group-horizontal">
        <dl class="col-4 pt-4">
          <ul>
            <li class="list-group-item"><span class="text-left "><b>Employees</b> <span class ="text-right" style="color:#42b983"> {{metadata.fullTimeEmployees }} </span></span></li>
            <!-- Use this one ^^-->
            <!-- <li class="list-group-item"><span class="text-left "><b>Employees</b> <span style="color:#42b983" class="">  </span></span></li> -->
            <!-- <div class="result">  </div></div> -->

            <li class="list-group-item"><span class="text-left "><b>Headquarters</b> <span class ="text-right" style="color:#42b983">{{metadata.city}}, {{metadata.state}}</span></span></li>
            <!-- Use this one ^^-->
            <!-- <li class="list-group-item"><span class="text-left "><b>Headquarters</b> <span style="color:#42b983" class="">  </span></span></li> -->
            <!-- <div class="result">Palo Alto, CA </div></div> -->

          </ul>
        </dl>
        <dl class="col-4 pt-4">
          <ul>

            <li class="list-group-item"><span class="text-left "><b>Market Cap</b> <span class ="text-right" style="color:#42b983">{{fundamentals.marketCap.fmt }}</span></span></li>

            <!-- <li class="list-group-item"><span class="text-left "><b>Market Cap</b> <span style="color:#42b983" class=""></span></span></li> -->
            <!-- Use this one ^^-->
            <!-- <div class="result"> 126.62B </div></div> -->

            <li class="list-group-item"><span class="text-left "><b>Average Volume</b> <span class ="text-right" style="color:#42b983"> {{fundamentals.averageVolume.fmt }}</span></span></li>
            <!-- <li class="list-group-item"><span class="text-left "><b>Average Volume</b> <span style="color:#42b983" class=""> </span></span></li> -->
            <!-- Use this one ^^-->
            <!-- <div class="result"> 20.72M </div></div> -->

          </ul>
        </dl>
        <dl class="col-4 pt-4">
          <ul>

            <li class="list-group-item"><span class="text-left "><b>52 Week High</b> <span style="color:#42b983" class="">{{fundamentals.fiftyTwoWeekHigh.fmt }}</span></span></li>
            <!-- <li class="list-group-item"><span class="text-left "><b>52 Week High</b> <span style="color:#42b983" class=""></span></span></li> -->
            <!-- Use this one ^^-->
            <!-- <div class="result"> 968.99 </div></div> -->

            <li class="list-group-item"><span class="text-left "><b>52 Week Low</b> <span style="color:#42b983" class="">{{fundamentals.fiftyTwoWeekLow.fmt }}</span></span></li>
            <!-- <li class="list-group-item"><span class="text-left "><b>52 Week Low</b> <span style="color:#42b983" class=""></span></span></li> -->
            <!-- Use this one ^^-->
            <!-- <div class="result"> 176.99 </div></div> -->
          </ul>
        </dl>

      </div>
    </b-row>
    <b-row>
      <div class = "col-12 pl-4 pr-4 ">
        <p class = "text-left text-muted h6 card p-4">
          {{metadata.longBusinessSummary }}
        </p>
        <!-- Use this one ^^-->
        <!-- <div class="section-description"> Tesla, Inc. designs, develops, manufactures, leases, and sells electric vehicles, and energy generation and storage systems in the United States, China, Netherlands, Norway, and internationally. The company operates in two segments, Automotive; and Energy Generation and Storage. The Automotive segment offers sedans and sport utility vehicles. It also provides electric powertrain components and systems; and services for electric vehicles through its company-owned service locations, and Tesla mobile service technicians, as well as sells used vehicles. This segment markets and sells its products through a network of company-owned stores and galleries, as well as through its own Website. The Energy Generation and Storage segment offers energy storage products, such as rechargeable lithium-ion battery systems for use in homes, industrial, commercial facilities, and utility grids; and designs, manufactures, installs, maintains, leases, and sells solar energy generation and energy storage products to residential and commercial customers. It also provides vehicle insurance services, as well as renewable energy. The company was formerly known as Tesla Motors, Inc. and changed its name to Tesla, Inc. in February 2017. Tesla, Inc. was founded in 2003 and is headquartered in Palo Alto, California.</div> -->
      </div>
    </b-row>

  </div>
</template>
<script>
import {mapGetters} from 'vuex'
export default {
  name: 'company-card',
  props: {
    custom: {
      type: String,
      default: ''
    },
    ticker: {
      type: String,
      default: ''
    },
  },
  data(){
    return {
      metadata: {
        longBusinessSummary : '--',
        fullTimeEmployees : '--',
        metadata : '--',
        state : '--'
      },
      fundamentals : {
        marketCap : {fmt : '--'},
        averageVolume : {fmt : '--'},
        fiftyTwoWeekHigh : {fmt : '--'},
        fiftyTwoWeekLow : {fmt : '--'}
      }
    }
  },
  async mounted(){
    var tick = '/'
    tick = tick + this.ticker
    //this.metadata = (await this.$http(this.$backendUrl + tick +'/metadata')).data
    //this.fundamentals = (await this.$http(this.$backendUrl + tick +'/fundamentals')).data
  },
  computed: mapGetters({
    metadata: 'getMetadata',
    fundamentals: 'getFundamentals'
  })
}
</script>
