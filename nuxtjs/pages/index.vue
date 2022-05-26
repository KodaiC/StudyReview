<template id="top">
  <v-app>
    <v-main>
      <v-container>
        <v-row class="ma-0 mb-5">
          <v-col class="col-12">
          </v-col>
          <h3 class="text-center">急上昇アカウント</h3>
          <v-tooltip bottom>
            <template v-slot:activator="{on, attrs}">
              <v-icon
                v-bind="attrs"
                v-on="on"
                class="ml-5"
              >
                mdi-help-circle
              </v-icon>
            </template>
            <span>
              ここでは1週間以内の評価のみが表示されています<br>
              ユーザーページなどで表示される評価とは違う可能性があります
            </span>
          </v-tooltip>
        </v-row>
        <v-row justify="center" justify-md="start" align="start">
          <template v-for="(user, index) in trendingUsers">
            <div
              class="col-11 col-md-6 mb-10"
              v-observe-visibility="(isVisible, entry) => onTrendingVisibilityChanged(isVisible, entry, user.id.replaceAll('-', ''))"
              style="min-height: 840px"
            >
              <UserCard
                :user="user"
                v-if="trendingIsVisible[user.id.replaceAll('-', '')]"
                style="min-height: 840px"
              />
            </div>
            <div
              class="col-11 col-md-6 mb-10"
              v-if="adv !== 0 && index % adv === adv - 1"
              v-observe-visibility="(isVisible, entry) => onTrendingVisibilityChanged(isVisible, entry, index)"
            >
              <v-card v-if="trendingIsVisible[index]">
                <v-card-text>aaaaaaaaaa</v-card-text>
              </v-card>
            </div>
          </template>
        </v-row>

        <h3 class="mb-5 mt-16">新規アカウント</h3>
        <v-row justify="center" justify-md="start" align="start">
          <template v-for="(user, index) in newUsers">
            <div
              class="col-11 col-md-6 mb-10"
              v-observe-visibility="(isVisible, entry) => onNewVisibilityChanged(isVisible, entry, user.id.replaceAll('-', ''))"
              style="min-height: 840px"
            >
              <UserCard
                :user="user"
                v-if="newIsVisible[user.id.replaceAll('-', '')]"
                style="min-height: 840px"
              />
            </div>
            <div
              class="col-11 col-md-6 mb-10"
              v-if="adv !== 0 && index % adv === adv - 1"
              v-observe-visibility="(isVisible, entry) => onNewVisibilityChanged(isVisible, entry, index)"
            >
              <v-card v-if="newIsVisible[index]">
                <v-card-text>aaaaaaaaaa</v-card-text>
              </v-card>
            </div>
          </template>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import UserCard from "../components/UserCard";

export default {
  name: "Homepage",
  components: {UserCard},
  auth: false,

  head: {
    title: "ホーム"
  },

  data() {
    return {
      trendingUsers: [],
      newUsers: [],
      trendingIsVisible: {},
      newIsVisible: {},
      adv: 0,
    };
  },

  beforeCreate() {
    this.$axios.get("users/?sort=-sum&date_rated=P1W&limit=30", {transformRequest: (data, headers) => {
        delete headers.common.Authorization;
        delete headers.Authorization;
        return data;
      }})
      .then(response => {
        this.trendingUsers = response.data.results;
      })
      .catch(e => {
        console.log(e);
      });

    this.$axios.get("users/?sort=-date_joined&limit=30", {transformRequest: (data, headers) => {
        delete headers.common.Authorization;
        delete headers.Authorization;
        return data;
      }})
      .then(response => {
        this.newUsers = response.data.results;
      })
      .catch(e => {
        console.log(e);
      });
    },

    methods: {
      onTrendingVisibilityChanged(isVisible, entry, id) {
        this.$set(this.trendingIsVisible, id, isVisible);
      },
      onNewVisibilityChanged(isVisible, entry, id) {
        this.$set(this.newIsVisible, id, isVisible);
      }
    }
};
</script>
