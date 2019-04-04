<template>
  <v-flex xs8 id="app" style="margin: auto">
    <v-btn
      slot="activator"
      color="primary"
      dark
      @click.native="loadProject">
      Load
    </v-btn>
    <v-data-table
      :headers="headersProject"
      :items="dataProject"
      hide-actions
      class="elevation-1"
    >
      <template slot="items" slot-scope="props">
        <td v-for="(item, index) in props.item" :key="index">
          {{ item }}
        </td>
        <td class="justify-center layout px-0">
          <v-btn
            slot="activator"
            color="primary"
            dark
            @click="predictItem(props.item)">
            predict
          </v-btn>
        </td>
      </template>
    </v-data-table>
    <div>
      <v-flex xs8 id="textfield">
        <v-text-field
          id="demo-field"
          name="text-input"
      label="ID Projet"
      single-line
      @click.native="onClickInput"
      v-model="value"
    ></v-text-field>
      </v-flex>
      <v-flex xs12>
        <v-btn
          slot="activator"
          color="primary"
          dark
          @click.native="predict">
          Predict
        </v-btn>
      </v-flex>
      <v-data-table
      :headers="headers"
      :items="data"
      hide-actions
      class="elevation-1"
    >
      <template slot="items" slot-scope="props">
        <td v-for="(item, index) in props.item" :key="index">
          <img v-if="index == 'picture'" :src="item"/>
          <span v-else>{{ item }}</span>
        </td>
      </template>
    </v-data-table>
    </div>
  </v-flex>
</template>

<script>
export default {
  name: 'HelloWorld',
  data() {
    return {
      value: null,
      headers: [
        { text: 'Day', value: 'friday' },
        { text: 'Name', value: 'name' },
        { text: 'Picture', value: 'picture' },
      ],
      headersProject: [
        { text: 'ID Projet', value: 'id' },
        { text: 'Nom', value: 'name' },
      ],
      data: [],
      dataProject: [],

    };
  },
  methods: {
    onClickInput() {
      this.$emit('setLock', true);
    },
    predict() {
      this.axios.get(`/define_croissanists/${this.value}/1`).then((response) => {
        if (response && response.data) {
          this.data = response.data;
        }
      }).catch(() => {
        this.response = 'Message invalide';
      });
    },
    loadProject() {
      this.axios.get('projects/load').then((response) => {
        if (response && response.data) {
          this.dataProject = response.data;
        }
      }).catch(() => {
        this.response = 'Message invalide';
      });
    },
    predictItem(item) {
      this.value = item.id;
      this.predict();
    },
  },
};
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
