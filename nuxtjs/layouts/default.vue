<template>
  <v-app>
    <v-navigation-drawer
      v-model="drawer"
      fixed
      app
      temporary
    >
      <v-list>
        <v-list-item
          v-for="(item, i) in items"
          :key="i"
          :to="item.to"
          router
          exact
        >
          <v-list-item-action>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title v-text="item.title"/>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar
      fixed
      app
    >
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"/>
      <v-toolbar-title @click="$router.push('/')" style="cursor:pointer" v-text="title"/>
      <v-spacer/>
      <v-icon
        class="mr-5"
        @click="theme = !theme">
        {{ theme ? "mdi-moon-waxing-crescent" : "mdi-white-balance-sunny" }}
      </v-icon>
      <v-btn
        v-if="!$store.state.auth.loggedIn"
        color="light-blue"
        outlined
        @click="$router.push('/login')"
      >
        ログイン
      </v-btn>

      <v-menu
        bottom
        min-width="200px"
        rounded
        offset-y
        v-else
      >
        <template v-slot:activator="{ on }">
          <v-btn
            icon
            x-large
            v-on="on"
            class="ma-2"
          >
            <v-avatar size="48" v-if="$auth.user.icon !== null" class="ma-2">
              <v-img
                :src="$auth.user.icon"
                max-width="128"
                max-height="128"
              />
            </v-avatar>
            <v-avatar size="48" :color="getUserColor($auth.user.username)" v-else class="ma-2">
              <v-icon size="40">mdi-account</v-icon>
            </v-avatar>
          </v-btn>
        </template>
        <v-card>
          <v-list-item-content class="justify-center">
            <div class="mx-auto text-center">
              <v-avatar size="56" v-if="$auth.user.icon !== null" class="ma-2">
                <v-img
                  :src="$auth.user.icon"
                  max-width="128"
                  max-height="128"
                />
              </v-avatar>
              <v-avatar size="56" :color="getUserColor($auth.user.username)" v-else class="ma-2">
                <v-icon size="50">mdi-account</v-icon>
              </v-avatar>
              <h3>{{ $auth.user.username }}</h3>
              <p class="text-caption mt-1">
                {{ $auth.user.email }}
              </p>
              <v-divider/>
              <v-btn
                block
                text
                @click="$router.push('mypage')"
                class="py-5"
              >
                マイページ
              </v-btn>
              <v-divider/>
              <v-btn
                block
                text
                @click="logout"
                class="py-5"
              >
                ログアウト
              </v-btn>
            </div>
          </v-list-item-content>
        </v-card>
      </v-menu>
    </v-app-bar>

    <v-main>
      <v-container>
        <Nuxt/>
      </v-container>
    </v-main>

    <v-footer class="mt-10">
      <v-row justify="space-around" class="ma-5">
        <div class="text-center text-md-justify col-12 col-md-auto">
          <h4>Study Review</h4>
          <p>&copy;2022 cogon</p>
        </div>
        <div class="text-center text-md-justify col-12 col-md-auto">
          <NuxtLink to="tos">利用規約</NuxtLink>
          <br>
          <NuxtLink to="policy">プライバシーポリシー</NuxtLink>
        </div>
        <div class="text-center text-md-justify col-12 col-md-auto">
          <a href="https://twitter.com/StudyReviewInfo" target="_blank">Twitter</a><br>
          <a href="mailto:studyreview.info@gmail.com">メールアドレス</a><br>
          <a href="https://forms.gle/a7jUXDLhyfi4ZAWQ9" target="_blank">お問い合わせフォーム</a>
        </div>
      </v-row>
    </v-footer>
  </v-app>
</template>

<script>
export default {
  name: "DefaultLayout",

  data() {
    return {
      drawer: false,
      items: [
        {
          icon: "mdi-home",
          title: "ホーム",
          to: "/"
        },
        {
          icon: "mdi-account-circle",
          title: "マイページ",
          to: "/mypage"
        },
        {
          icon: "mdi-magnify",
          title: "検索",
          to: "/search",
        },
      ],
      title: "Study Review",
      theme: this.$store.state.theme,
    };
  },

  beforeCreate() {
    this.$store.state.theme = Boolean(this.$cookies.get("theme"));
    this.$vuetify.theme.dark = this.$store.state.theme;
  },

  methods: {
    getUserColor(username) {
      const colors = ["red", "pink", "purple", "blue", "light-blue", "cyan", "green", "light-green", "lime", "yellow", "amber", "orange"];
      let sum = 0;
      for (let i = 0; i < username.length; i++) {
        sum += username.codePointAt(i);
      }

      return colors[sum % colors.length];
    },
    logout() {
      this.$auth.logout();
      this.$toasted.success("ログアウトしました", {
        theme: "bubble",
        position: "top-center",
        duration: 3000,
      });
    }
  },

  watch: {
    theme() {
      this.$store.dispatch("theme", this.theme);
      this.$vuetify.theme.dark = this.theme;
      this.$cookies.set("theme", this.theme, {path: "/", maxAge: 2147483647});
    },
  },
};
</script>
