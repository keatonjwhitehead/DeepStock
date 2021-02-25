<template>
  <div>
    <div class="card text-center">
      <div class="card-body twitter-card-body" style = "max-height: 250px; overflow-y: scroll;">
        <div class = "tweet-card-tweet" style = "background: #f1f1f1; padding: 10px; border-radius: 5px;margin-bottom: 15px;box-shadow: 0px 2px 1px -1px rgba(0,0,0,0.2), 0px 1px 1px 0px rgba(0,0,0,0.14), 0px 1px 3px 0px rgba(0,0,0,0.12);" v-for="tweet in tweets" :key="tweet">
          {{ tweet }}
        </div>
      </div>
      <div class="card-footer text-muted">
       Recent {{ticker}} Tweets
      </div>
    </div>
  </div>
</template>
<script>
import {mapGetters} from 'vuex'

export default {
  name: 'twitter-card',
  props: {
    custom: {
      type: String,
      default: ''
    },
    ticker: {
      type: String,
      default: ''
    }
  },
  data(){
    return {
    }
  },
  computed: mapGetters({tweets: 'getTweetText', ticker: 'getTicker'})
}
</script>
