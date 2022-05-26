<template>
  <v-app>
    <v-main>
      <v-container>
        <v-form class="ma-5">
          <v-text-field
            v-model="user.username"
            label="ユーザーネーム"
            maxlength="150"
            outlined
            counter
          />
          <small class="text--secondary" v-if="user.type === 'teacher'">自己紹介</small>
          <div v-if="user.type === 'teacher' && isReady" class="mb-8">
            <editor
              :apiKey="$config.TMCE_TOKEN"
              :init="{
                menubar: false,
                external_plugins: {
                  'youtube': '/tinymce-plugin-youtube-3.0.0/plugin.js'
                },
                plugins: [
                  'autolink lists link image charmap preview',
                  'fullscreen hr',
                  'table wordcount',
                  'youtube'
                ],
                toolbar:
                  'undo redo | formatselect | bold italic strikethrough forecolor backcolor charmap | \
                  alignleft aligncenter alignright alignjustify | \
                  youtube link unlink | \
                  bullist numlist table outdent indent hr | removeformat | fullscreen preview',
                language: 'ja',
                language_url: 'ja.js',
                height: 500,
                toolbar_mode: 'scrolling',
                skin: this.$store.state.theme ? 'oxide-dark' : '',
                content_css: this.$store.state.theme ? 'dark' : '',
                elementpath: false,
                extend_valid_elements: 'client-only,lite-youtube[videoid|params|class|playlabel],div[class]',
                content_css: 'lite-youtube-embed/lite-yt-embed.css',
                setup: function(ed) {
                  ed.on('init', function() {
                    let head = ed.dom.select('head')[0];
                    ed.dom.add(
                      head,
                      'script',
                      {
                        src: 'lite-youtube-embed/lite-yt-embed.js',
                        type: ('text/javascript')
                      }
                    )
                  });
                }
              }"
              v-model="user.introduction"
            />
          </div>
          <v-select
            v-model="user.content"
            label="コンテンツタイプ"
            outlined
            :items="contents"
            v-if="user.type === 'teacher'"
          />
          <v-select
            v-model="user.subjects"
            :items="subjects"
            chips
            label="教科"
            multiple
            outlined
            v-if="user.type === 'teacher'"
          />
          <v-text-field
            v-model="user.url"
            :error-messages="urlErrors"
            label="URL"
            @input="$v.user.url.$touch()"
            @blur="$v.user.url.$touch()"
            outlined
            type="url"
            v-if="user.type === 'teacher'"
          />
          <input
            type="file"
            accept="image/*"
            @change="onChangeFile"
            style="display: none;"
            ref="iconInput"
          />
          <v-col>
            <v-row justify="space-between" justify-md="start">
              <v-btn @click="$refs.iconInput.click()" class="mr-5">
                アイコン選択
              </v-btn>
              <v-btn @click="deleteIcon">
                アイコン削除
              </v-btn>
            </v-row>
          </v-col>
          <v-col>
            <v-row justify="center" justify-md="start">
              <v-img
                max-height="256"
                max-width="256"
                class="ma-4 ml-0"
                :src="iconUrl"
                v-if="iconUrl !== null"
              />
              <p v-else class="mt-5">アイコンなし</p>
            </v-row>
          </v-col>
          <v-row class="ma-0 mb-1" v-if="user.type === 'teacher'" align-content="end">
            <p class="text-center ma-0 pa-0" style="padding-top: 3px">タグ</p>
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
              タグは検索だけでなく、SNSでシェアする際にも使われます<br>
              使われるタグは最初の3つのみが使われます<br>
              ドラッグで順番を変えることが出来ます
            </span>
          </v-tooltip>
          </v-row>
          <draggable
            v-if="user.type === 'teacher'"
            v-model="user.ordered_tags"
            :options="{animation: 200, handle: '.draggable', delay: 50, delayOnTouchOnly: true}"
            element="v-chip-group"
            column
          >
            <v-chip
              v-for="(tag, i) in user.ordered_tags"
              close
              :key="i"
              @click:close="deleteTag(tag)"
              style="cursor: move"
              class="draggable ma-1"
            >
              {{ tag }}
            </v-chip>
          </draggable>
          <v-text-field
            v-model.trim="currentTag"
            label="新しいタグの追加"
            append-icon="mdi-plus"
            @click:append="addTag"
            maxlength="32"
            counter
            outlined
            class="mt-1"
            @keyup.enter="addTag"
            v-if="user.type === 'teacher'"
          />
          <div v-if="user.type === 'student'" class="my-7">
            <h5>評価履歴</h5>
            <v-simple-table
              :style="`background-color: ${this.$store.state.theme ? '#121212' : '#FFFFFF'}`"
              fixed-header
              :height="rated.length > 5 ? '300px' : ''"
            >
              <template v-slot:default>
                <thead>
                <tr>
                  <th class="text-left">
                    ユーザーネーム
                  </th>
                  <th class="text-left">
                    評価日
                  </th>
                  <th></th>
                </tr>
                </thead>
                <tbody>
                <tr
                  v-for="rating in user.rated"
                  :key="rating.id"
                  @click="$router.push(`user/${rating.ratee}`)"
                >
                  <td>{{ rating.ratee_name }}</td>
                  <td>{{ getDateStr(rating.date_rated) }}</td>
                  <td>
                    <v-icon>mdi-open-in-new</v-icon>
                  </td>
                </tr>
                </tbody>
              </template>
            </v-simple-table>
          </div>

          <v-row justify="center" justify-md="end" class="mt-10">
            <v-btn
              @click="update"
              class="ma-3 col-11 col-md-auto"
              :disabled="$v.user.url.$invalid"
            >
              保存
            </v-btn>
          </v-row>

          <v-row justify="center" justify-md="space-between" class="mt-10">
            <v-btn
              outlined
              color="red"
              class="ma-3 col-11 col-md-auto"
              @click="logout"
            >
              ログアウト
            </v-btn>
            <v-dialog v-model="emailDialog" width="600">
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  outlined
                  color="red"
                  class="ma-3 col-11 col-md-auto"
                  v-bind="attrs"
                  v-on="on"
                >
                  メールアドレス変更
                </v-btn>
              </template>

              <v-card>
                <v-card-title class="text-h5">
                  メールアドレス変更
                </v-card-title>
                <v-card-text class="mt-3">
                  <p class="text--primary">
                    現在のメールアドレスは{{ user.email }}です。<br>
                    {{ user.email }}宛てに変更のためのURLが送信されます。<br>
                    そのURLにアクセスすることでメールアドレスを変更することができます。<br>
                    メールアドレスを変更しますか？<br>
                  </p>
                </v-card-text>
                <v-card-actions>
                  <v-row justify="end" class="ma-0">
                    <v-btn
                      text
                      @click="emailDialog = false">
                      取り消し
                    </v-btn>
                    <v-btn
                      text
                      @click="changeEmail"
                    >
                      変更
                    </v-btn>
                  </v-row>
                </v-card-actions>
              </v-card>
            </v-dialog>

            <v-dialog v-model="passwordDialog" width="600">
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  outlined
                  color="red"
                  class="ma-3 col-11 col-md-auto"
                  v-bind="attrs"
                  v-on="on"
                >
                  パスワード変更
                </v-btn>
              </template>

              <v-card>
                <v-card-title class="text-h5">
                  パスワード変更
                </v-card-title>
                <v-card-text class="mt-3">
                  <v-form @submit.prevent>
                    <v-text-field
                      v-model="currentPassword"
                      :error-messages="currentPasswordErrors"
                      :append-icon="currentPasswordShow ? 'mdi-eye' : 'mdi-eye-off'"
                      :type="currentPasswordShow ? 'text' : 'password'"
                      label="現在のパスワード"
                      required
                      @input="() => {this.$v.currentPassword.$touch(); this.currentPasswordError = ''}"
                      @blur="() => {this.$v.currentPassword.$touch(); this.currentPasswordError = ''}"
                      @click:append="currentPasswordShow = !currentPasswordShow"
                      outlined
                    />
                    <v-text-field
                      v-model="newPassword"
                      :error-messages="newPasswordErrors"
                      :append-icon="newPasswordShow ? 'mdi-eye' : 'mdi-eye-off'"
                      :type="newPasswordShow ? 'text' : 'password'"
                      label="新しいパスワード"
                      @input="() => {$v.newPassword.$touch(); this.newPasswordError = '';}"
                      @blur="() => {$v.newPassword.$touch(); this.newPasswordError = '';}"
                      @click:append="newPasswordShow = !newPasswordShow"
                      outlined
                    />
                    <v-text-field
                      v-model="reNewPassword"
                      :error-messages="reNewPasswordErrors"
                      :append-icon="reNewPasswordShow ? 'mdi-eye' : 'mdi-eye-off'"
                      :type="reNewPasswordShow ? 'text' : 'password'"
                      label="新しいパスワード(再入力)"
                      @input="$v.reNewPassword.$touch()"
                      @blur="$v.reNewPassword.$touch()"
                      @click:append="reNewPasswordShow = !reNewPasswordShow"
                      outlined
                      @keyup.enter="() => {if (!$v.currentPassword.$invalid && !$v.newPassword.$invalid && !$v.reNewPassword.$invalid && newPassword === reNewPassword) changePassword()}"
                    />
                  </v-form>
                </v-card-text>
                <v-card-actions>
                  <v-row justify="end" class="ma-0">
                    <v-btn
                      text
                      @click="passwordDialog = false">
                      取り消し
                    </v-btn>
                    <v-btn
                      text
                      @click="changePassword"
                      :disabled="$v.currentPassword.$invalid || $v.newPassword.$invalid || $v.reNewPassword.$invalid || newPassword !== reNewPassword"
                    >
                      変更
                    </v-btn>
                  </v-row>
                </v-card-actions>
              </v-card>
            </v-dialog>

            <v-dialog v-model="deleteDialog" width="600">
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  outlined
                  color="red"
                  class="ma-3 col-11 col-md-auto"
                  v-bind="attrs"
                  v-on="on"
                >
                  アカウント削除
                </v-btn>
              </template>

              <v-card>
                <v-card-title class="text-h5">
                  警告
                </v-card-title>
                <v-card-text>
                  <p class="text--primary">
                    削除したアカウントは元に戻せません<br>
                    削除しますか？
                  </p>
                  <v-form @submit.prevent>
                    <v-text-field
                      v-model="deletePassword"
                      :error-messages="deletePasswordErrors"
                      :append-icon="deleteShow ? 'mdi-eye' : 'mdi-eye-off'"
                      :type="deleteShow ? 'text' : 'password'"
                      label="パスワード"
                      required
                      @input="$v.deletePassword.$touch()"
                      @blur="$v.deletePassword.$touch()"
                      @click:append="deleteShow = !deleteShow"
                      outlined
                    />
                  </v-form>
                </v-card-text>
                <v-card-actions>
                  <v-row justify="end" class="ma-0">
                    <v-btn
                      text
                      @click="deleteDialog = false">
                      取り消し
                    </v-btn>
                    <v-btn
                      color="red"
                      text
                      @click="deleteAccount"
                      :disabled="$v.deletePassword.$invalid"
                    >
                      削除
                    </v-btn>
                  </v-row>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </v-row>
        </v-form>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import FormData from "form-data";
import {validationMixin} from "vuelidate";
import {url, minLength, required} from "vuelidate/lib/validators";
import _cloneDeep from "lodash/cloneDeep";

export default {
  mixins: [validationMixin],

  validations: {
    user: {
      url: {url, required},
    },
    deletePassword: {required, minLength: minLength(8),},
    currentPassword: {required, minLength: minLength(8),},
    newPassword: {required, minLength: minLength(8),},
    reNewPassword: {required, minLength: minLength(8)}
  },

  name: "mypage",
  auth: true,

  head: {
    title: "マイページ"
  },

  data() {
    return {
      contents: [
        {"text": "YouTube", "value": "youtube"},
        {"text": "その他動画サイト", "value": "video"},
        {"text": "ウェブサイト", "value": "web"}
      ],
      subjects: [
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
      fileData: null,
      fileUrl: null,
      currentTag: "",
      user: {},
      deleteDialog: false,
      deletePassword: "",
      emailDialog: false,
      passwordDialog: false,
      currentPassword: "",
      newPassword: "",
      reNewPassword: "",
      deleteShow: false,
      currentPasswordShow: false,
      newPasswordShow: false,
      reNewPasswordShow: false,
      currentPasswordError: "",
      newPasswordError: "",
      doDeleteIcon: false,
      isReady: false,
      selection: null,
    };
  },

  async mounted() {
    await this.$axios.get("auth/users/me/")
      .then(response => {
        this.user = _cloneDeep(response.data);
        this.$auth.setUser(_cloneDeep(response.data));
        this.isReady = true;
      })
      .catch(e => {
        console.log(e);
      });
  },

  computed: {
    iconUrl() {
      return this.fileUrl === null ? this.user.icon : this.fileUrl;
    },
    urlErrors() {
      const errors = [];
      if (!this.$v.user.url.$dirty) return errors;
      if (!this.$v.user.url.url) errors.push("有効なURLを入力してください");
      if (!this.$v.user.url.required) errors.push("URLを入力してください");
      return errors;
    },
    deletePasswordErrors() {
      const errors = [];
      if (!this.$v.deletePassword.$dirty) return errors;
      if (!this.$v.deletePassword.minLength) errors.push("パスワードは8文字以上です");
      if (!this.$v.deletePassword.required) errors.push("パスワードを入力してください");
      return errors;
    },
    currentPasswordErrors() {
      const errors = [];
      if (!this.$v.currentPassword.$dirty) return errors;
      if (!this.$v.currentPassword.minLength) errors.push("パスワードは8文字以上です");
      if (!this.$v.currentPassword.required) errors.push("パスワードを入力してください");
      if (this.currentPasswordError !== "") errors.push(this.currentPasswordError);
      return errors;
    },
    newPasswordErrors() {
      const errors = [];
      if (!this.$v.newPassword.$dirty) return errors;
      if (!this.$v.newPassword.minLength) errors.push("パスワードは8文字以上です");
      if (!this.$v.newPassword.required) errors.push("パスワードを入力してください");
      if (this.newPasswordError !== "") errors.push(this.newPasswordError);
      return errors;
    },
    reNewPasswordErrors() {
      const errors = [];
      if (!this.$v.reNewPassword.$dirty) return errors;
      if (!this.$v.reNewPassword.minLength) errors.push("パスワードは8文字以上です");
      if (!this.$v.reNewPassword.required) errors.push("パスワードを入力してください");
      if (this.newPassword !== this.reNewPassword) errors.push("パスワードが一致しません");
      return errors;
    },
    rated() {
      const rateds = [];
      for (let i = 0; i < 2; i++) {
        rateds.push({
          id: i,
          ratee: {id: i},
          ratee_name: i + "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
          date_rated: "2022-03-01T09:46:03+09:00"
        });
      }

      return rateds;
    }
  },

  watch: {
    deleteDialog() {
      this.deletePassword = "";
      this.$v.$reset();
    },
    passwordDialog() {
      this.currentPassword = "";
      this.newPassword = "";
      this.reNewPassword = "";
      this.$v.$reset();
    }
  },

  methods: {
    async update() {
      let formData = new FormData();

      let f = true;

      if (this.fileData !== null) {
        formData.append(
          "icon",
          new Blob([this.fileData.data], {type: this.fileData.type}),
          this.fileData.fileName
        );

        const config = {
          headers: {
            "Content-type": "multipart/form-data",
          },
        };

        await this.$axios.patch("auth/users/me/", formData, config)
          .then(response => {
            this.user.icon = response.data.icon;
            this.$auth.setUser(_cloneDeep(this.user));
            this.file = null;
            this.fileData = null;
            this.fileUrl = null;
            f = true;
          })
          .catch(e => {
            console.log(e);
            f = false;
          });
      }

      const request_data = {...this.user,};
      if (this.doDeleteIcon) {
        request_data.icon = null;
        this.doDeleteIcon = false;
      } else delete request_data.icon;
      delete request_data.rated;
      delete request_data.ratings;
      delete request_data.tags;
      delete request_data.email;
      delete request_data.id;
      delete request_data.type;

      await this.$axios.patch("auth/users/me/", request_data)
        .then(response => {
          f = f && true;
          this.$auth.setUser(_cloneDeep(this.user));
        })
        .catch(e => {
          console.log(e);
          f = false;
        });

      if (f) {

        this.$toasted.success("保存しました", {
          theme: "bubble",
          position: "top-center",
          duration: 3000,
        });
      } else {
        this.$toasted.error("保存に失敗しました", {
          theme: "bubble",
          position: "top-center",
          duration: 3000,
        });
      }
    },
    onChangeFile(event) {
      let selectedFile = event.target.files[0];

      if (!selectedFile) {
        this.fileData = null;
        this.fileUrl = "";
        return;
      }

      this.fileData = {};
      this.fileData.type = selectedFile.type;
      this.fileData.fileName = selectedFile.name;

      this.readFileAsync(selectedFile)
        .then(result => {
          this.fileData.data = result;
        })
        .catch(error => {
          this.$toasted.error("ファイルの読み込みに失敗しました", {
            theme: "bubble",
            position: "top-center",
            duration: 3000,
          });
        });

      this.readFileUrl(selectedFile)
        .then(result => {
          this.fileUrl = result;
        })
        .catch(error => {
          this.$toasted.error("ファイルの読み込みに失敗しました", {
            theme: "bubble",
            position: "top-center",
            duration: 3000,
          });
        });
    },
    readFileAsync(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => {
          resolve(reader.result);
        };
        reader.onerror = reject;
        reader.readAsArrayBuffer(file);
      });
    },
    readFileUrl(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => {
          resolve(reader.result);
        };
        reader.onerror = reject;
        reader.readAsDataURL(file);
      });
    },
    deleteIcon() {
      this.fileData = null;
      this.fileUrl = null;
      this.doDeleteIcon = true;
      this.user.icon = null;
    },
    deleteTag(tag) {
      this.user.ordered_tags = this.user.ordered_tags.filter(t => t !== tag);
    },
    addTag() {
      const tag = this.currentTag.replace(/\s/g, "");
      if (!this.user.ordered_tags.includes(tag)) this.user.ordered_tags.push(tag);
      this.currentTag = "";
    },
    async deleteAccount() {
      this.deleteDialog = false;
      await this.$axios.$delete("auth/users/me/", {data: {current_password: this.deletePassword}})
        .then(response => {
          this.$toasted.success("アカウントを削除しました", {
            theme: "bubble",
            position: "top-center",
            duration: 3000,
          });
          this.$auth.logout();
          this.$router.push("/");
        })
        .catch(e => {
          console.log(e);
          this.$toasted.error(`${e.request.responseText === "{\"current_password\":[\"Invalid password.\"]}" ? "パスワードが違います" : "アカウントの削除に失敗しました"}`, {
            theme: "bubble",
            position: "top-center",
            duration: 3000,
          });
        });
    },
    async changeEmail() {
      this.emailDialog = false;
      await this.$axios.$post("auth/users/reset_email/", {email: this.user.email})
        .then(response => {
          this.$toasted.success("現在のメールアドレスに変更のURLを送信しました", {
            theme: "bubble",
            position: "top-center",
            duration: 3000,
          });
        })
        .catch(e => {
          console.log(e);
          this.$toasted.error("エラーが発生しました", {
            theme: "bubble",
            position: "top-center",
            duration: 3000,
          });
        });
    },
    async changePassword() {
      await this.$axios.$post("auth/users/set_password/", {
        current_password: this.currentPassword,
        new_password: this.newPassword,
        re_new_password: this.reNewPassword
      })
        .then(response => {
          this.passwordDialog = false;
          this.$toasted.success("パスワードを変更しました", {
            theme: "bubble",
            position: "top-center",
            duration: 3000,
          });
        })
        .catch(e => {
          console.log(e);
          if (e.response) {
            let invalidPassword = false;
            if (e.response.data.current_password !== undefined) {
              if (e.response.data.current_password[0] === "Invalid password.") invalidPassword = true;
              else this.currentPasswordError = e.response.data.current_password[0];
            }
            if (e.response.data.new_password !== undefined) {
              if (e.response.data.new_password[0] === "このパスワードは一般的すぎます。") this.newPasswordError = "このパスワードは簡単すぎます";
              else if (e.response.data.new_password[0] === "このパスワードは email と似すぎています。") this.newPasswordError = "このパスワードはメールアドレスと似すぎています";
              else if (e.response.data.new_password[0] === "このパスワードは username と似すぎています。") this.newPasswordError = "このパスワードはユーザーネームと似すぎています";
              else this.newPasswordError = e.response.data.new_password[0];
            }

            if (invalidPassword) this.$toasted.error("パスワードが違います", {
              theme: "bubble",
              position: "top-center",
              duration: 3000,
            });
            else if (this.currentPasswordError === "" && this.newPasswordError === "") {
              this.$toasted.error("パスワードの変更に失敗しました", {
                theme: "bubble",
                position: "top-center",
                duration: 3000,
              });
              this.passwordDialog = false;
            }
          }
        });
    },
    logout() {
      this.$auth.logout();
      this.$toasted.success("ログアウトしました", {
        theme: "bubble",
        position: "top-center",
        duration: 3000,
      });
    },
    getDateStr(date) {
      const d = new Date(date);
      return `${d.getFullYear()}/${d.getMonth()}/${d.getDate()}`;
    },
  }
};
</script>

<style scoped>

</style>
