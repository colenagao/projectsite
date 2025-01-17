<template>
    <div class="grid">
        <div v-for="item in items" class="cell">
          <div class="card">
            <div class="card-image">
              <figure class="image is-4by3">
                <img :src="'/img/' + item.fileName">
              </figure>
            </div>
            <div class="card-content">
          
              <div class="content">
                {{ item.description }}
                <br />
              </div>
            </div>
          </div>
        </div>
      </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
  name: 'About',
  data() {
    return {
        items: [
        { fileName: 'climbing.jpg', description: "High Plains Drifter, Buttermilks - Bishop, CA" },
        { fileName: 'skiing.JPG', description: "Sunshine Village, Banff, Canada" },
        { fileName: 'camping.JPG', description: "Moab, Utah" }
        ],
    };
  },
};
  </script>