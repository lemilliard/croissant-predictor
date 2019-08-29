<template>
  <v-flex xs8 id="app" style="margin: auto">
    <h1>CroissantPredictor</h1>
    <v-progress-circular v-if="loading" style="margin-top: 50px;"
      indeterminate
      color="primary"
    ></v-progress-circular>
    <v-data-table style="margin-top: 50px;"
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
      <v-layout row wrap style="margin-top: 20px; margin-bottom:20px">
        <v-flex xs4 id="id-textfield">
          <v-text-field
            id="id-field"
            name="text-input"
            label="ID Projet"
            @click.native="onClickInput"
            v-model="value"
          ></v-text-field>
        </v-flex>
        <v-flex xs2 id="textfield" style="margin: auto">
            <v-text-field
              id="nb-croissanist-field"
              name="text-input"
              label="Nb croissanist"
              @click.native="onClickInput"
              v-model="nbCroissanist"
            ></v-text-field>
        </v-flex>
        <v-flex xs2 id="textfield_months" style="margin: auto">
            <v-text-field
              id="months-field"
              name="text-input"
              label="Nb months"
              @click.native="onClickInput"
              v-model="nbMonths"
            ></v-text-field>
        </v-flex>
      </v-layout>
      <v-layout row wrap>
        <v-flex xs4>
          <v-btn v-if="value!=null"
            slot="activator"
            color="primary"
            dark
            @click.native="loadPersons">
            Persons
          </v-btn>
          <v-data-table v-if="dataPersons.length > 0" style="margin-bottom:20px"
            :headers="headersPersons"
            :items="dataPersons"
            hide-actions
            class="elevation-1"
            v-model="selected"
            select-all
            item-key="name"
          >
            <template slot="items" slot-scope="props">
              <td>
                <v-checkbox
                  v-model="props.selected"
                  primary
                  hide-details
                ></v-checkbox>
              </td>
              <td>
                {{ props.item.name }}
              </td>
            </template>
          </v-data-table>
        </v-flex>
        <v-flex xs8 style="padding-left:10px">
          <v-btn v-if="value!=null"
            slot="activator"
            color="primary"
            dark
            @click.native="predict">
            Predict
          </v-btn>
          <v-data-table v-if="data.length > 0"
          :headers="headers"
          :items="data"
          hide-actions
          class="elevation-1"
          >
            <template slot="items" slot-scope="props">
              <td v-for="header in headers" :key="header.value">
                <img v-if="header.value == 'picture'" :src="props.item[header.value]"/>
                <span v-else>{{ props.item[header.value] }}</span>
              </td>
            </template>
          </v-data-table>
        </v-flex>
      </v-layout>
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
      nbMonths: 1,
      headers: [
        { text: 'Day', value: 'friday', align: 'center' },
        { text: 'Name', value: 'name', align: 'center' },
        { text: 'Email', value: 'email', align: 'center' },
        { text: 'Picture', value: 'picture', align: 'center' },
      ],
      headersProject: [
        { text: 'ID Projet', value: 'id', align: 'center' },
        { text: 'Nom', value: 'name', align: 'center' },
      ],
      headersPersons: [
        { text: 'Name', value: 'name', align: 'center' },
      ],
      data: [],
      dataProject: [],
      dataPersons: [],
      selected: [],
      personSelected: [],
      loading: false,
    };
  },
  created() {
    this.loadProject();
  },
  methods: {
    onClickInput() {
      this.$emit('setLock', true);
    },
    predict() {
      this.loading = true;
      this.personSelected = [];
      this.selected.forEach((e) => {
        this.personSelected.push(e.name);
      });
      if (this.personSelected.length > 0) {
        this.axios.post(`/define_croissanists_with_filter/${this.value}/${this.nbMonths}/${this.nbCroissanist}`, this.personSelected).then((response) => {
          if (response && response.data) {
            this.data = response.data;
            this.loading = false;
          }
        }).catch(() => {
          this.response = 'Message invalide';
          this.loading = false;
        });
      } else {
        this.axios.get(`/define_croissanists/${this.value}/${this.nbMonths}/${this.nbCroissanist}`).then((response) => {
          if (response && response.data) {
            this.data = response.data;
            this.loading = false;
          }
        }).catch(() => {
          this.response = 'Message invalide';
          this.loading = false;
        });
      }
    },
    loadProject() {
      this.loading = true;
      this.axios.get('projects/load').then((response) => {
        if (response && response.data) {
          this.dataProject = response.data;
          this.loading = false;
        }
      }).catch(() => {
        this.response = 'Message invalide';
        this.loading = false;
      });
    },
    selectItem(item) {
      this.value = item.id;
    },
    loadPersons() {
      this.loading = true;
      this.axios.get(`/persons/${this.value}/1`).then((response) => {
        if (response && response.data) {
          this.dataPersons = response.data;
          this.loading = false;
        }
      }).catch(() => {
        this.response = 'Message invalide';
        this.loading = false;
      });
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
