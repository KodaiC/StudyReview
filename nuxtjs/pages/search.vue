<template>
  <v-app>
    <v-main>
      <v-container>
        <v-row justify="center">
          <v-text-field
            solo
            label="タグ検索"
            class="col-11 col-md-8"
            append-icon="mdi-magnify"
            @click:append="search(true)"
            v-model="searchTags"
            @keyup.enter="search(true)"
          />

          <v-expansion-panels class="col-11 col-md-8 pa-0 mb-8">
            <v-expansion-panel class="ma-0">
              <v-expansion-panel-header>
                詳細検索
              </v-expansion-panel-header>
              <v-expansion-panel-content>
                <v-form>
                  <v-select
                    v-model="contents"
                    chips
                    label="コンテンツタイプ"
                    multiple
                    outlined
                    :items="contentSelects"
                  />
                  <v-select
                    v-model="subjects"
                    chips
                    label="教科"
                    multiple
                    outlined
                    :items="subjectSelects"
                  />
                  <v-text-field
                    v-model="understandability"
                    label="分かりやすさ"
                    outlined
                    suffix="以上"
                    type="number"
                    min="0"
                    max="5"
                  />
                  <v-text-field
                    v-model="usefulness"
                    label="お役立ち度"
                    outlined
                    suffix="以上"
                    type="number"
                    min="0"
                    max="5"
                  />
                  <v-text-field
                    v-model="fun"
                    label="面白さ"
                    outlined
                    suffix="以上"
                    type="number"
                    min="0"
                    max="5"
                  />
                  <v-text-field
                    v-model="count"
                    label="評価数"
                    outlined
                    suffix="以上"
                    type="number"
                    min="0"
                  />
                  <v-select
                    v-model="sort"
                    label="並び替え"
                    outlined
                    :items="sortSelects"
                  />
                </v-form>
                <v-row justify="end" class="ma-0">
                  <v-btn @click="search(true)">検索</v-btn>
                </v-row>
              </v-expansion-panel-content>
            </v-expansion-panel>
          </v-expansion-panels>
        </v-row>

        <h1 id="dummyResult" class="ma-0 pa-0" style="white-space: pre-wrap">{{ " " }}</h1>
        <h3 class="mt-10 mb-5" v-if="isSearched && users.length !== 0">検索結果</h3>
        <v-row justify="center" v-if="isSearched && users.length === 0" class="my-16">
          <h3>条件に当てはまるユーザーはいませんでした</h3>
        </v-row>
        <v-row justify="center" justify-md="start">
          <template v-for="(user, index) in users">
            <div
              class="col-11 col-md-6 mb-10"
              style="min-height: 840px"
              v-observe-visibility="(isVisible, entry) => onVisibilityChanged(isVisible, entry, user.id.replaceAll('-', ''))"
            >
              <UserCard
                :user="user"
                style="min-height: 840px"
                v-if="isVisible[user.id.replaceAll('-', '')]"
              />
            </div>
            <div class="col-11 col-md-6 mb-10" v-if="adv !== 0 && index % adv === adv - 1">
              <v-card>
                <v-card-text>aaaaaaaaaa</v-card-text>
              </v-card>
            </div>
          </template>
        </v-row>

        <v-row justify="center" class="ma-10" v-if="isSearched && users.length !== 0">
          <v-pagination
            v-model="page"
            :length="Math.ceil(number / limit)"
            :total-visible="7"
          />
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: "search",
  auth: false,

  head: {
    title: "検索"
  },

  data() {
    return {
      searchTags: "",
      page: 1,
      users: [],
      isSearched: false,
      understandability: "",
      usefulness: "",
      fun: "",
      count: "",
      contents: [],
      contentSelects: [
        {"text": "YouTube", "value": "youtube"},
        {"text": "その他動画サイト", "value": "video"},
        {"text": "ウェブサイト", "value": "web"}
      ],
      sort: "",
      sortSelects: [
        {"text": "高評価順", "value": "-sum"},
        {"text": "評価数順", "value": "-count"},
        {"text": "新着順", "value": "-date_joined"},
        {"text": "ランダム", "value": "random"},
        {"text": "指定なし", "value": ""}
      ],
      subjects: [],
      subjectSelects: [
        {"text": "国語", "value": "japanese"},
        {"text": "現代文", "value": "contemp_jp"},
        {"text": "古典", "value": "classics"},

        {"text": "英語", "value": "english"},

        {"text": "算数", "value": "elem_math"},
        {"text": "数学", "value": "math"},
        {"text": "数学ⅠA", "value": "math_1a"},
        {"text": "数学ⅡB", "value": "math_2b"},
        {"text": "数学Ⅲ", "value": "math_3"},

        {"text": "理科", "value": "science"},
        {"text": "物理", "value": "physics"},
        {"text": "化学", "value": "chemistry"},
        {"text": "生物", "value": "biology"},
        {"text": "地学", "value": "earth_science"},

        {"text": "社会", "value": "social_studies"},
        {"text": "地理", "value": "geography"},
        {"text": "歴史", "value": "history"},
        {"text": "世界史", "value": "world_history"},
        {"text": "日本史", "value": "jp_history"},
        {"text": "公民", "value": "civics"},
        {"text": "現代社会", "value": "contmp_society"},
        {"text": "倫理", "value": "ethics"},
        {"text": "政治・経済", "value": "politics_economy"},

        {"text": "芸術", "value": "art"},
        {"text": "保健体育", "value": "hp_education"},
        {"text": "家庭科", "value": "home_economics"},

        {"text": "その他", "value": "other"},
      ],
      limit: 30,
      number: 0,
      adv: 0,
      isVisible: {},
    };
  },

  created() {
    this.searchTags = this.$route.query.searchTags || "";
    if (this.$route.query.contents) this.contents = [this.$route.query.contents];
    if (this.$route.query.subjects) this.subjects = [this.$route.query.subjects];
    if (this.searchTags !== "" || this.contents.length !== 0 || this.subjects.length !== 0) this.search(false);
  },

  watch: {
    "$route"(to, from) {
      this.searchTags = this.$route.query.searchTags || "";
      if (this.$route.query.contents) this.contents = [this.$route.query.contents];
      if (this.$route.query.subjects) this.subjects = [this.$route.query.subjects];
      if (this.searchTags !== "" || this.contents.length !== 0 || this.subjects.length !== 0) this.search(false);
    },
    page() {
      this.search(true);
    }
  },

  methods: {
    search(doScroll) {
      const tags = this.searchTags.split(/\s/).filter(t => t !== "").join(",");
      this.isSearched = false;

      let url = `users/?limit=${this.limit}&offset=${(this.page - 1) * this.limit}&` +
                (tags !== "" ? `tags=${tags}&` : "") +
                (this.understandability !== "" ? `understandability=${this.understandability}&` : "") +
                (this.usefulness !== "" ? `usefulness=${this.usefulness}&` : "") +
                (this.fun !== "" ? `fun=${this.fun}&` : "") +
                (this.count !== "" ? `count=${this.count}&` : "") +
                (this.contents.length !== 0 ? `content=${this.contents.join("&content=")}&` : "") +
                (this.subjects.length !== 0 ? `subjects=${this.subjects.join(",")}&` : "") +
                (this.sort !== "" && this.sort !== "random" ? `sort=${this.sort}&` : "") +
                (this.sort === "random" ? "random=1" : "");

      this.$axios.get(url, {
        transformRequest: (data, headers) => {
          delete headers.common.Authorization;
          delete headers.Authorization;
          return data;
        }
      })
        .then(response => {
          this.users = response.data.results;
          this.number = response.data.count;
          this.isSearched = true;
        })
        .catch(e => {
          console.log(e);
        });

      if (doScroll) this.$scrollTo("#dummyResult", 500);
    },
    onVisibilityChanged(isVisible, entry, id) {
      this.$set(this.isVisible, id, isVisible);
    },
  }
};
</script>

<style scoped>

</style>
