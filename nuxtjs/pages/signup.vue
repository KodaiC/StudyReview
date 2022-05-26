<template>
  <v-app>
    <v-main>
      <v-container>
        <v-form v-if="!isSent">
          <v-row justify="center">
            <v-col cols="12" md="8">
              <v-card>
                <v-container>
                  <v-row justify="center">
                    <h2 class="ma-5">新規アカウント登録</h2>
                    <v-col cols="11">
                      <v-text-field
                        v-model="email"
                        :error-messages="emailErrors"
                        label="メールアドレス"
                        @input="() => {$v.email.$touch(); this.emailError = ''}"
                        @blur="() => {$v.email.$touch(); this.emailError = ''}"
                        outlined
                      />
                      <v-text-field
                        v-model="username"
                        label="ユーザーネーム"
                        outlined
                        maxlength="150"
                        counter
                        :error-messages="usernameErrors"
                        @input="$v.username.$touch()"
                        @blur="$v.username.$touch()"
                      />
                      <v-select
                        v-model="type"
                        label="アカウントタイプ"
                        outlined
                        :items="types"
                      />
                      <v-select
                        v-model="content"
                        label="コンテンツタイプ"
                        outlined
                        :items="contents"
                        v-if="type === 'teacher'"
                      />
                      <v-text-field
                        v-model="url"
                        label="URL"
                        outlined
                        :error-messages="urlErrors"
                        v-if="type === 'teacher'"
                        @input="$v.url.$touch()"
                        @blur="$v.url.$touch()"
                      />
                      <v-text-field
                        v-model="password"
                        :error-messages="passwordErrors"
                        :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
                        :type="show ? 'text' : 'password'"
                        label="パスワード"
                        @input="() => {$v.password.$touch(); this.passwordError = ''}"
                        @blur="() => {$v.password.$touch(); this.passwordError = ''}"
                        @click:append="show = !show"
                        outlined
                      />
                      <v-text-field
                        v-model="rePassword"
                        :error-messages="rePasswordErrors"
                        :append-icon="reShow ? 'mdi-eye' : 'mdi-eye-off'"
                        :type="reShow ? 'text' : 'password'"
                        label="パスワード(再入力)"
                        @input="$v.rePassword.$touch()"
                        @blur="$v.rePassword.$touch()"
                        @click:append="reShow = !reShow"
                        outlined
                      />
                      <v-checkbox v-model="agree">
                        <template v-slot:label>
                          <div>
                            <a href="tos" target="_blank" @click.stop>利用規約</a>及び<a href="policy" target="_blank" @click.stop>プライバシーポリシー</a>に同意する
                          </div>
                        </template>
                      </v-checkbox>
                    </v-col>
                  </v-row>
                  <v-row justify="end" align="center">
                    <v-btn
                      :disabled="
                        (this.type === 'student' && ($v.email.$invalid || $v.password.$invalid || $v.rePassword.$invalid)) ||
                        (this.type === 'teacher' && $v.$invalid) ||
                        password !== rePassword || !agree"
                      class="ma-5 ma-md-10"
                      @click="signup"
                    >
                      登録
                    </v-btn>
                  </v-row>
                </v-container>
              </v-card>
            </v-col>
          </v-row>
        </v-form>
        <v-row justify="center" v-else>
          <v-col>
            <h4 class="text-center ma-3">確認メールを送信しました</h4>
            <h4 class="text-center ma-3">届かない場合は<NuxtLink to="/activate">ここ</NuxtLink>からメールを再送できます</h4>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import {validationMixin} from 'vuelidate';
import {required, email, minLength, maxLength, url} from 'vuelidate/lib/validators';

export default {
  mixins: [validationMixin],

  validations: {
    email: {required, email},
    password: {required, minLength: minLength(8),},
    rePassword: {required, minLength: minLength(8),},
    username: {required, maxLength: maxLength(150)},
    url: {required, url}
  },

  head: {
    title: "新規アカウント登録",
  },

  name: "signup",
  auth: false,

  data() {
    return {
      email: "",
      password: "",
      rePassword: "",
      username: "",
      type: "teacher",
      url: "",
      content: "youtube",
      show: false,
      reShow: false,
      isSent: false,
      agree: false,
      emailError: "",
      passwordError: "",
      types: [
        {"text": "先生", "value": "teacher"},
        {"text": "学生", "value": "student"}
      ],
      contents: [
        {"text": "YouTube", "value": "youtube"},
        {"text": "その他動画サイト", "value": "video"},
        {"text": "ウェブサイト", "value": "web"}
      ],
    }
  },

  computed: {
    emailErrors() {
      const errors = [];
      if (!this.$v.email.$dirty) return errors;
      if (!this.$v.email.email) errors.push("有効なメールアドレスを入力してください");
      if (!this.$v.email.required) errors.push("メールアドレスを入力してください");
      if (this.emailError !== "") errors.push(this.emailError);
      return errors;
    },
    passwordErrors() {
      const errors = [];
      if (!this.$v.password.$dirty) return errors;
      if (!this.$v.password.minLength) errors.push("パスワードは8文字以上です");
      if (!this.$v.password.required) errors.push("パスワードを入力してください");
      if (this.passwordError !== "") errors.push(this.passwordError);
      return errors;
    },
    rePasswordErrors() {
      const errors = [];
      if (!this.$v.rePassword.$dirty) return errors;
      if (!this.$v.rePassword.minLength) errors.push("パスワードは8文字以上です");
      if (!this.$v.rePassword.required) errors.push("パスワードを入力してください");
      if (this.password !== this.rePassword) errors.push("パスワードが一致しません");
      return errors;
    },
    usernameErrors() {
      const errors = [];
      if (!this.$v.username.$dirty) return errors;
      if (!this.$v.username.maxLength) errors.push("ユーザーネームは150文字以下です");
      if (!this.$v.username.required) errors.push("ユーザーネームを入力してください");
      return errors;
    },
    urlErrors() {
      const errors = [];
      if (!this.$v.url.$dirty) return errors;
      if (!this.$v.url.url) errors.push("有効なURLを入力してください")
      if (!this.$v.url.required) errors.push("URLを入力してください");
      return errors;
    }
  },

  methods: {
    signup() {
      this.$axios.$post("auth/users/",
        {
          email: this.email,
          username: this.username,
          type: this.type,
          content: this.content,
          url: this.type === "student" ? "https://studyreview.cogon-k.com" : this.url,
          password: this.password,
          re_password: this.rePassword
        },
        {
          "headers": {
            "Content-Type": "application/json",
            "Authorization": ""
          }
        })
        .then(response => {
          this.isSent = true;
        })
        .catch(e => {
          console.log(e);
          if (e.response) {
            if (e.response.data.email !== undefined) {
              if (e.response.data.email[0] === "この email を持った user が既に存在します。") this.emailError = "このメールアドレスは既に使われています";
              else this.emailError = e.response.data.email[0];
            }
            if (e.response.data.password !== undefined) {
              if (e.response.data.password[0] === "このパスワードは一般的すぎます。") this.passwordError = "このパスワードは簡単すぎます";
              else if (e.response.data.password[0] === "このパスワードは email と似すぎています。") this.passwordError = "このパスワードはメールアドレスと似すぎています";
              else if (e.response.data.password[0] === "このパスワードは username と似すぎています。") this.passwordError = "このパスワードはユーザーネームと似すぎています";
              else this.passwordError = e.response.data.password[0];
            }
          }

          if (this.emailError === "" && this.passwordError === "") {
            this.$toasted.error("エラーが発生しました", {
              theme: "bubble",
              position: "top-center",
              duration: 3000,
            });
          }
        });
    },
  }
};
</script>

<style scoped>

</style>
