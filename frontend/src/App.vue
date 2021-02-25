<template>
  <div id="app">
    <div id="nav">
      <!--img src='@/assets/imgs/logo.png' width=100 height=100 style="margin-right:10px;"-->
      <b-row>
        <b-col class="col-2"></b-col>
        <b-col class="col-1">
          <img src='@/assets/imgs/logo2.png' width=80 height=100 style="margin-right:10px;">
        </b-col>
        <b-col class="col-3">
          <b-row>
            <h1 style="display:inline; color: white;">DeepBroth</h1>
          </b-row>
          <b-row>
            <router-link to="/">Dashboard </router-link>
            <a style="padding-left:1em "></a>|<a style="padding-right:1em "></a>
            <router-link to="/about">About </router-link>
          </b-row>
        </b-col>
      </b-row>
    </div>
    <router-view/>
  </div>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  text-align:left;
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
