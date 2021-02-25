<template>
  <div class="about container">
    <h1 class="text-light">Developers</h1>
    <b-row>
      <div class="offset-lg-1"></div>
      <info-card name="Jake Andrus" github = "JakeAndrus" href="https://github.com/JakeAndrus" image = "../assets/imgs/img_avatar1.png" bio = "Talk to me to insert your bio"/>
      <info-card-2 name="Natnael Abraha" github = "natnaelmesfun" href="https://github.com/natnaelmesfun" image = "../assets/imgs/img_avatar1.png" bio = "Talk to me to insert your bio"/>
      <info-card name="Zora Watters" github = "zorawatters" href="https://github.com/zorawatters" image = "../assets/imgs/img_avatar2.png" bio = "Talk to me to insert your bio"/>
    </b-row>
    <b-row>
      <div class="offset-lg-1"></div>
      <info-card name="Oscar Delgado" github = "oscardel13" href="https://github.com/oscardel13" image = "../assets/imgs/img_avatar1.png" bio = "Talk to me to insert your bio"/>
      <info-card-2 name="Kyle Faucher" github = "kylefaucher" href="https://github.com/kylefaucher" image = "../assets/imgs/img_avatar1.png" bio = "Talk to me to insert your bio"/>
      <info-card name="Keaton Whitehead" github = "keatonjwhitehead" href="https://github.com/keatonjwhitehead" image = "../assets/imgs/keaton_pic.jpg" bio = "Senior at the University of Colorado studying Computer Science"/>
    </b-row>

  </div>
</template>
<script>
  import InfoCard from '@/components/InfoCard.vue'
  import InfoCard2 from '@/components/InfoCard2.vue'
  export default {
    name: 'about',
    components: {
      'info-card': InfoCard,
      'info-card-2':InfoCard2
    }
  }
</script>
