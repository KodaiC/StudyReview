<template>
  <v-app>
    <v-main>
      <v-container class="col-12 col-md-8">
        <v-row justify="center">
          <v-avatar size="128" v-if="user.icon !== null">
            <v-img
              :src="user.icon"
              max-width="128"
              max-height="128"
            />
          </v-avatar>
          <v-avatar
            size="128"
            :color="getUserColor(user.username)"
            v-else
          >
            <v-icon size="112">mdi-account</v-icon>
          </v-avatar>
        </v-row>
        <v-row justify="center" class="my-6">
          <v-col>
            <h2 class="text-center ma-0 pa-0 my-2 col-12 break">{{ user.username }}</h2>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <div v-html="html" class="ma-0 pa-0 my-6 break col-12" id="introduction"/>
          </v-col>
        </v-row>

        <v-row class="mr-0">
          <v-col>
            <a :href="user.url" class="ml-1" target="_blank">{{ user.url }}</a>
          </v-col>
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
              このURLは各ユーザーが登録したものです<br>
              不審なURLが登録されていた場合、お問い合わせフォームなどからご連絡ください
            </span>
          </v-tooltip>
        </v-row>

        <v-row>
          <v-col class="mt-4">
            <p class="ma-1 pa-0 ml-1 mb-5">評価数: {{ user.count }}</p>
            <p class="ma-0 pa-0 ml-1">分かりやすさ</p>
            <v-expansion-panels class="mb-2" :flat="true">
              <v-expansion-panel>
                <v-expansion-panel-header class="pa-0" :color="this.$store.state.theme ? '#121212' : '#FFFFFF'">
                  <client-only>
                    <star-rating
                      :increment="0.01"
                      :read-only="true"
                      :star-size="22"
                      :rounded-corners="true"
                      :border-width="2"
                      :padding="3"
                      :border-color="this.$store.state.theme ? '#5C6BC0' : '#999'"
                      :inactive-color="this.$store.state.theme ? '#1E1E1E' : '#d8d8d8'"
                      :active-color="this.$store.state.theme ? '#5C6BC0' : '#FFD055'"
                      v-model="user.understandability"
                    />
                  </client-only>
                </v-expansion-panel-header>
                <v-expansion-panel-content class="pa-0" :color="this.$store.state.theme ? '#121212' : '#FFFFFF'">
                  <v-list flat disabled class="pa-0" :color="this.$store.state.theme ? '#121212' : '#FFFFFF'">
                    <v-list-item-group
                      v-for="(und_item, i) in user.understandability_dist"
                      :key="`und_${i}`"
                      class="pa-0"
                    >
                      <v-list-item dense class="pa-0">
                        <v-list-item-icon>
                          <v-icon>mdi-star</v-icon>
                          {{ i }}
                        </v-list-item-icon>
                        <v-list-item-content>{{ und_item }}人</v-list-item-content>
                      </v-list-item>
                    </v-list-item-group>
                  </v-list>
                </v-expansion-panel-content>
              </v-expansion-panel>
            </v-expansion-panels>
            <p class="ma-0 pa-0 ml-1">お役立ち度</p>
            <v-expansion-panels class="mb-2" :flat="true">
              <v-expansion-panel>
                <v-expansion-panel-header class="pa-0" :color="this.$store.state.theme ? '#121212' : '#FFFFFF'">
                  <client-only>
                    <star-rating
                      :increment="0.01"
                      :read-only="true"
                      :star-size="22"
                      :rounded-corners="true"
                      :border-width="2"
                      :padding="3"
                      :border-color="this.$store.state.theme ? '#5C6BC0' : '#999'"
                      :inactive-color="this.$store.state.theme ? '#1E1E1E' : '#d8d8d8'"
                      :active-color="this.$store.state.theme ? '#5C6BC0' : '#FFD055'"
                      v-model="user.usefulness"
                    />
                  </client-only>
                </v-expansion-panel-header>
                <v-expansion-panel-content class="pa-0" :color="this.$store.state.theme ? '#121212' : '#FFFFFF'">
                  <v-list flat disabled class="pa-0" :color="this.$store.state.theme ? '#121212' : '#FFFFFF'">
                    <v-list-item-group
                      v-for="(use_item, i) in user.usefulness_dist"
                      :key="`use_${i}`"
                      class="pa-0"
                    >
                      <v-list-item dense class="pa-0">
                        <v-list-item-icon>
                          <v-icon>mdi-star</v-icon>
                          {{ i }}
                        </v-list-item-icon>
                        <v-list-item-content>{{ use_item }}人</v-list-item-content>
                      </v-list-item>
                    </v-list-item-group>
                  </v-list>
                </v-expansion-panel-content>
              </v-expansion-panel>
            </v-expansion-panels>
            <p class="ma-0 pa-0 ml-1">面白さ</p>
            <v-expansion-panels class="mb-2" :flat="true">
              <v-expansion-panel>
                <v-expansion-panel-header class="pa-0" :color="this.$store.state.theme ? '#121212' : '#FFFFFF'">
                  <client-only>
                    <star-rating
                      :increment="0.01"
                      :read-only="true"
                      :star-size="22"
                      :rounded-corners="true"
                      :border-width="2"
                      :padding="3"
                      :border-color="this.$store.state.theme ? '#5C6BC0' : '#999'"
                      :inactive-color="this.$store.state.theme ? '#1E1E1E' : '#d8d8d8'"
                      :active-color="this.$store.state.theme ? '#5C6BC0' : '#FFD055'"
                      v-model="user.fun"
                    />
                  </client-only>
                </v-expansion-panel-header>
                <v-expansion-panel-content class="pa-0" :color="this.$store.state.theme ? '#121212' : '#FFFFFF'">
                  <v-list flat disabled class="pa-0" :color="this.$store.state.theme ? '#121212' : '#FFFFFF'">
                    <v-list-item-group
                      v-for="(fun_item, i) in user.fun_dist"
                      :key="`fun_${i}`"
                      class="pa-0"
                    >
                      <v-list-item dense class="pa-0">
                        <v-list-item-icon>
                          <v-icon>mdi-star</v-icon>
                          {{ i }}
                        </v-list-item-icon>
                        <v-list-item-content>{{ fun_item }}人</v-list-item-content>
                      </v-list-item>
                    </v-list-item-group>
                  </v-list>
                </v-expansion-panel-content>
              </v-expansion-panel>
            </v-expansion-panels>
          </v-col>
        </v-row>

        <v-row>
          <v-chip-group column class="ma-4 mb-3 ml-3">
            <v-chip
              :ripple="false"
              @click.stop="$router.push(`/search?contents=${user.content}`)"
            >
              <v-icon left color="grey lighten-3" v-if="$store.state.theme">mdi-link-variant</v-icon>
              <v-icon left color="grey darken-2" v-else>mdi-link-variant</v-icon>
              {{ contents[user.content] }}
            </v-chip>
            <v-chip
              v-for="subject in user.subjects"
              :ripple="false"
              @click.stop="$router.push(`/search?subjects=${subject}`)"
              :key="subject"
            >
              <v-icon left color="grey lighten-3" v-if="$store.state.theme">mdi-lead-pencil</v-icon>
              <v-icon left color="grey darken-2" v-else>mdi-lead-pencil</v-icon>
              {{subjects[subject]}}
            </v-chip>
            <v-chip
              v-for="tag in user.ordered_tags"
              :ripple="false"
              :key="tag"
              @click="$router.push(`/search?searchTags=${tag}`)">
              <v-icon left color="grey lighten-3" v-if="$store.state.theme">mdi-tag</v-icon>
              <v-icon left color="grey darken-2" v-else>mdi-tag</v-icon>
              {{ tag }}
            </v-chip>
          </v-chip-group>
        </v-row>

        <v-row
          class="mt-10"
          justify="space-between"
          align="center"
          v-if="$auth.loggedIn && $auth.user.type === 'student'"
        >
          <v-col>
            <h4 class="mb-2 ml-1">評価する</h4>
            <p class="ma-0 pa-0 ml-1">分かりやすさ</p>
            <client-only>
              <star-rating
                :star-size="22"
                :rounded-corners="true"
                :border-width="2"
                :padding="3"
                :border-color="this.$store.state.theme ? '#5C6BC0' : '#999'"
                :inactive-color="this.$store.state.theme ? '#1E1E1E' : '#d8d8d8'"
                :active-color="this.$store.state.theme ? '#5C6BC0' : '#FFD055'"
                :active-on-click="false"
                v-model="understandability"
                class="mb-2"
              />
            </client-only>
            <p class="ma-0 pa-0 ml-1">お役立ち度</p>
            <client-only>
              <star-rating
                :star-size="22"
                :rounded-corners="true"
                :border-width="2"
                :padding="3"
                :border-color="this.$store.state.theme ? '#5C6BC0' : '#999'"
                :inactive-color="this.$store.state.theme ? '#1E1E1E' : '#d8d8d8'"
                :active-color="this.$store.state.theme ? '#5C6BC0' : '#FFD055'"
                :active-on-click="false"
                v-model="usefulness"
                class="mb-2"
              />
            </client-only>
            <p class="ma-0 pa-0 ml-1">面白さ</p>
            <client-only>
              <star-rating
                :star-size="22"
                :rounded-corners="true"
                :border-width="2"
                :padding="3"
                :border-color="this.$store.state.theme ? '#5C6BC0' : '#999'"
                :inactive-color="this.$store.state.theme ? '#1E1E1E' : '#d8d8d8'"
                :active-color="this.$store.state.theme ? '#5C6BC0' : '#FFD055'"
                :active-on-click="false"
                v-model="fun"
              />
            </client-only>
          </v-col>

          <v-row class="col-4 mr-3 mr-md-0" justify="center">
            <v-btn
              class="my-4"
              @click="rate"
              :disabled="understandability === 0 || usefulness === 0 || fun === 0"
            >
              {{ rated ? "評価を変更する" : "評価する" }}
            </v-btn>
            <v-btn
              class="my-4"
              @click="deleteRating"
              :disabled="!rated"
            >
              評価を取り消す
            </v-btn>
          </v-row>
        </v-row>

        <v-row class="mt-10" justify="center">
          <h4 v-if="!$auth.loggedIn">評価するにはログインしてください</h4>
          <h4 v-else-if="$auth.user.type === 'teacher'">学生アカウントのみ評価することができます</h4>
        </v-row>

        <client-only>
          <v-row justify="center" justify-md="end" class="my-16 mr-md-1">
            <social-sharing
              :title="title"
              :hashtags="hashtags"
              twitter-user="StudyReviewInfo"
              :url="`https://studyreview.cogon-k.com${$route.path}`"
              inline-template
            >
              <div>
                <network network="twitter">
                  <div class="ma-1" style="display: inline-flex">
                    <fa class="share-button twitter text--white" :icon="['fab', 'twitter']" />
                  </div>
                </network>
                <network network="line">
                  <div class="ma-1" style="display: inline-flex">
                    <fa class="share-button line text--white" :icon="['fab', 'line']" />
                  </div>
                </network>
                <network network="facebook">
                  <div class="ma-1" style="display: inline-flex">
                    <fa class="share-button facebook text--white" :icon="['fab', 'facebook-f']" />
                  </div>
                </network>
                <network network="email">
                  <div class="ma-1 mr-0" style="display: inline-flex">
                    <fa class="share-button email text--white" :icon="['fas', 'envelope']" />
                  </div>
                </network>
              </div>
            </social-sharing>
          </v-row>
        </client-only>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: "id",
  auth: false,
  head: {
    title: "ユーザーページ"
  },

  data() {
    return {
      user: {},
      contents: {
        "youtube": "YouTube",
        "video": "動画サイト",
        "web": "ウェブサイト"
      },
      subjects: {
        "japanese": "国語",
        "contemp_jp": "現代文",
        "classics": "古典",

        "english": "英語",

        "elem_math": "算数",
        "math": "数学",
        "math_1a": "数学ⅠA",
        "math_2b": "数学ⅡB",
        "math_3": "数学Ⅲ",

        "science": "理科",
        "physics": "物理",
        "chemistry": "科学",
        "biology": "生物",
        "earth_science": "地学",

        "social_studies": "社会",
        "geography": "地理",
        "history": "歴史",
        "world_history": "世界史",
        "jp_history": "日本史",
        "civics": "公民",
        "contmp_society": "現代社会",
        "ethics": "倫理",
        "politics_economy": "政治・経済",

        "art": "芸術",
        "hp_education": "保健体育",
        "home_economics": "家庭科",

        "other": "その他",
      },
      understandability: 0,
      usefulness: 0,
      fun: 0,
      ratingId: null,
      rated: false
    };
  },

  beforeCreate() {
    this.$axios.get(`users/${this.$route.params.id}/`, {
      transformRequest: (data, headers) => {
        delete headers.common.Authorization;
        delete headers.Authorization;
        return data;
      }
    })
      .then(response => {
        this.user = response.data;
      })
      .catch(e => {
        console.log(e);
        if (e.response.status === 404) this.$router.push("/");
      });
  },

  computed: {
    html() {
      return this.$sanitize(
        (this.user.introduction + ""), {
          allowedIframeHostnames: ['www.youtube.com']
        }
      );
    },
    title() {
      return `${this.user.username} - Study Review`
    },
    hashtags() {
      let hashtags = ["StudyReview"];
      if (this.user.subjects !== undefined) {
        for (let i = 0; i < Math.min(2, this.user.subjects.length); i++) {
          hashtags.push(this.subjects[this.user.subjects[i]]);
        }
      }
      if (this.user.ordered_tags !== undefined) {
        for (let i = 0; i < Math.min(3, this.user.ordered_tags.length); i++) {
          hashtags.push(this.user.ordered_tags[i]);
        }
      }

      return hashtags.join(",");
    }
  },

  mounted() {
    if (this.$auth.loggedIn && this.$auth.user.rated !== null) {
      let rate = this.$auth.user.rated.filter(r => r.ratee === this.$route.params.id);
      if (rate.length === 1) {
        this.understandability = rate[0].understandability;
        this.usefulness = rate[0].usefulness;
        this.fun = rate[0].fun;
        this.ratingId = rate[0].id;
        this.rated = true;
      }
    }
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

    async rate() {
      if (this.ratingId !== null) {
        await this.$axios.$delete(`ratings/${this.ratingId}/`)
          .catch(e => {
            console.log(e);
          });
      }
      await this.$axios.$post("ratings/", {
        understandability: this.understandability,
        usefulness: this.usefulness,
        fun: this.fun,
        sum: this.understandability + this.usefulness + this.fun,
        ratee: this.$route.params.id
      })
        .then(response => {
          this.ratingId = response.id;
          this.rated = true;
          this.$toasted.success("評価しました", {
            theme: "bubble",
            position: "top-center",
            duration: 3000,
          });
        })
        .catch(e => {
          this.$toasted.error("評価に失敗しました", {
            theme: "bubble",
            position: "top-center",
            duration: 3000,
          });
          console.log(e);
        });

      this.$axios.get(`users/${this.$route.params.id}/`, {
        transformRequest: (data, headers) => {
          delete headers.common.Authorization;
          delete headers.Authorization;
          return data;
        }
      })
        .then(response => {
          this.user = response.data;
        })
        .catch(e => {
          console.log(e);
        });
    },

    async deleteRating() {
      if (this.ratingId !== null) {
        await this.$axios.$delete(`ratings/${this.ratingId}/`)
          .then(response => {
            this.ratingId = null;
            this.understandability = 0;
            this.usefulness = 0;
            this.fun = 0;
            this.rated = false;
            this.$toasted.success("評価を取り消しました", {
              theme: "bubble",
              position: "top-center",
              duration: 3000,
            });
          })
          .catch(e => {
            console.log(e);
            this.$toasted.error("評価の取り消しに失敗しました", {
              theme: "bubble",
              position: "top-center",
              duration: 3000,
            });
          });

        this.$axios.get(`users/${this.$route.params.id}/`, {
          transformRequest: (data, headers) => {
            delete headers.common.Authorization;
            delete headers.Authorization;
            return data;
          }
        })
          .then(response => {
            this.user = response.data;
          })
          .catch(e => {
            console.log(e);
          });
      }
    }
  }
};
</script>

<style scoped>
* >>> iframe {
  width: 100%;
  aspect-ratio: 16 / 10;
}
* >>> .share-button {
  cursor: pointer;
  outline: none;
  appearance: none;
  color: white;
  border-radius: 4px;
  box-shadow: 0 3px 3px rgba(0, 0, 0, 0.1);
  height: 28px;
  width: 28px;
  padding: 8px;
  overflow: visible;
  box-sizing: content-box;
}
* >>> .email {
  background-color: #952225;
}
* >>> .facebook {
  background-color: #3B569D;
}
* >>> .line {
  background-color: #45C405;
}
* >>> .twitter {
  background-color: #1DA1F2;
}

* >>> .break {
  overflow-wrap: break-word;
}

* >>> .break * {
  overflow-wrap: break-word;
}
</style>
