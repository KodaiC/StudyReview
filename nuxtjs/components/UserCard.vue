<template>
  <div ref="card">
    <v-card
      :ripple="false"
      class="px-4 py-2"
    >
      <v-row class="ma-0 pa-0">
        <div class="ma-4 mr-2">
          <v-avatar size="48" v-if="user.icon !== null">
            <v-img
              :src="user.icon"
              max-width="128"
              max-height="128"
            />
          </v-avatar>
          <v-avatar size="48" :color="getUserColor(user.username)" v-else>
            <v-icon size="40">mdi-account</v-icon>
          </v-avatar>
        </div>
        <v-col>
          <h4
            class="ma-0 pa-0 my-1"
            style="height: 48px; overflow: hidden; display: flex; word-break: break-all; align-items: center;"
          >
            {{ user.username }}
          </h4>
        </v-col>
      </v-row>
      <v-row class="ma-2 pa-0 ml-3" align="end">
        <v-col class="ma-0 pa-0 col-11">
          <div
            :class="`introduction${expandIntroduction ? ' open' : ''} ma-0 pa-0`"
            ref="introduction"
            v-html="html"
            :style="`overflow: hidden; ${expandIntroduction ? 'max-height: ' + introductionHeight + 'px;' : ''}`"
          />
        </v-col>
        <v-icon
          @click="() => {this.expandIntroduction = !this.expandIntroduction}"
          @click.stop
          v-show="expandIntroduction || introductionHeight > 300"
          :ripple="false"
          :class="`no-hover ${this.expandIntroduction ? 'rotate': ''} pa-1 col-1`"
        >
          mdi-chevron-down
        </v-icon>
      </v-row>
      <v-row class="ma-0">
        <v-col>
          <p class="ma-0 pa-0">評価数: {{user.count}}</p>
          <p class="ma-0 pa-0">分かりやすさ</p>
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
              v-model:rating="user.understandability"
              class="mb-2"
            />
          </client-only>
          <p class="ma-0 pa-0">お役立ち度</p>
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
              v-model:rating="user.usefulness"
              class="mb-2"
            />
          </client-only>
          <p class="ma-0 pa-0">面白さ</p>
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
              v-model:rating="user.fun"
              class="star"
            />
          </client-only>
        </v-col>
      </v-row>
      <v-row class="ma-2 pa-0 ml-3" align="end">
        <v-col class="ma-0 pa-0 col-11">
          <div
            :style="`overflow: hidden; ${expandTags ? 'max-height: ' + tagsHeight + 'px;' : ''}`"
            :class="`tags ${expandTags ? 'open' : ''} ma-0 pa-0 col-11`"
            ref="tags"
          >
            <v-chip-group column>
              <v-chip
                :ripple="false"
                @click.stop="$router.push(`/search?contents=${user.content}`)"
              >
                <v-icon left color="grey lighten-3" v-if="$store.state.theme">mdi-link-variant</v-icon>
                <v-icon left color="grey darken-2" v-else>mdi-link-variant</v-icon>
                {{contents[user.content]}}
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
                @click.stop="$router.push(`/search?searchTags=${tag}`)"
                :key="tag"
              >
                <v-icon left color="grey lighten-3" v-if="$store.state.theme">mdi-tag</v-icon>
                <v-icon left color="grey darken-2" v-else>mdi-tag</v-icon>
                {{tag}}
              </v-chip>
            </v-chip-group>
          </div>
        </v-col>
        <v-icon
          @click="() => {this.expandTags = !this.expandTags;}"
          @click.stop
          v-show="expandTags || tagsHeight > 88"
          :ripple="false"
          :class="`no-hover ${this.expandTags ? 'rotate': ''} pa-1 col-1`"
        >
          mdi-chevron-down
        </v-icon>
      </v-row>
      <v-row justify="end" class="ma-4 mt-8">
        <v-btn @click="$router.push(`/user/${user.id}`)">詳細を見る</v-btn>
      </v-row>
    </v-card>
  </div>
</template>

<script>
export default {
  name: "UserCard",
  props: ["user"],

  data() {
    return {
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
        "chemistry": "化学",
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
      expandIntroduction: false,
      expandTags: false,
      introductionHeight: 0,
      tagsHeight: 0,
      observer: null,
      isVisible: false
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
    computeHeight() {
      this.introductionHeight = (this.$refs.introduction && this.$refs.introduction.scrollHeight) ? this.$refs.introduction.scrollHeight : 300;
      this.tagsHeight = (this.$refs.tags && this.$refs.tags.scrollHeight) ? this.$refs.tags.scrollHeight : 88;
    }
  },

  computed: {
    html() {
      return this.$sanitize(
        (this.user.introduction + ""), {
          allowedIframeHostnames: ['www.youtube.com']
        }
      );
    },
  },

  mounted() {
    this.computeHeight();
    window.addEventListener("resize", this.computeHeight);
    this.observer = new ResizeObserver((entries) => {
      this.computeHeight();
    });
    this.observer.observe(this.$refs.card);
  },

  beforeDestroy() {
    this.observer.disconnect(this.$refs.card);
    window.removeEventListener("resize", this.computeHeight);
  }
};
</script>

<style scoped>
* >>> iframe {
  width: 100%;
  aspect-ratio: 16 / 10;
}

* >>> .introduction {
  transition: 0.4s cubic-bezier(0.25, 0.8, 0.5, 1), visibility 0s;
  max-height: 300px;
  min-height: 300px;
}

* >>> .tags {
  transition: 0.4s cubic-bezier(0.25, 0.8, 0.5, 1), visibility 0s;
  max-height: 88px;
  min-height: 88px;
}


* >>> .open {
  transition: 0.4s cubic-bezier(0.25, 0.8, 0.5, 1), visibility 0s;
}

* >>> .no-hover:after {
  background-color: transparent !important;
}

* >>> .rotate {
  transform: rotate(-180deg);
}
</style>
