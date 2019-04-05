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
            @click="selectItem(props.item)">
            Select
          </v-btn>
        </td>
      </template>
    </v-data-table>
    <div>
      <v-layout row wrap>
        <v-flex xs6 id="id-textfield">
          <v-text-field
            id="id-field"
            name="text-input"
            label="ID Projet"
            single-line
            @click.native="onClickInput"
            v-model="value"
          ></v-text-field>
        </v-flex>
        <v-flex xs3 id="textfield" style="margin: auto">
            <v-text-field
              id="nb-croissanist-field"
              name="text-input"
              label="Nb croissanist"
              single-line
              @click.native="onClickInput"
              v-model="nbCroissanist"
            ></v-text-field>
        </v-flex>
      </v-layout>
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
          <object v-if="index == 'picture'" :data="item" type="image/jpg"
            style="border-radius: 15px">
            <img style="width: 100px; border-radius: 15px"
              src="http://10.24.216.11:3000/img/collaborator/400x400/std_avatar.jpg"/>
          </object>
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
      nbCroissanist: 1,
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
      this.axios.get(`/define_croissanists/${this.value}/1/${this.nbCroissanist}`).then((response) => {
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
    selectItem(item) {
      this.value = item.id;
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
