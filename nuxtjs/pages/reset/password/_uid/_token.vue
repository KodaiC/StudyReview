<template>
  <v-main>
    <v-container>
      <v-row justify="center">
        <v-col>
          <h2 class="text-center ma-10">パスワード変更</h2>
          <h3 class="text-center" v-if="staled">
            トークンの期限が切れました<br>
            もう一度<NuxtLink to="/reset/password/">リセットページ</NuxtLink>から変更の手続きをやり直してください
          </h3>

          <v-form class="mt-10" v-if="!staled" @submit.prevent>
            <v-row justify="center">
              <v-col cols="11">
                <v-text-field
                  v-model="password"
                  :error-messages="passwordErrors"
                  :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
                  :type="show ? 'text' : 'password'"
                  label="パスワード"
                  @input="() => {$v.password.$touch(); this.passwordError = '';}"
                  @blur="() => {$v.password.$touch(); this.passwordError = '';}"
                  @click:append="show = !show"
                  outlined
                  v-if="$route.params.uid && $route.params.token"
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
                  @keyup.enter="() => {if (!$v.password.$invalid && !$v.rePassword.$invalid && this.password === this.rePassword) changePassword()}"
                  v-if="$route.params.uid && $route.params.token"
                />
                <v-text-field
                v-model="email"
                :error-messages="emailErrors"
                label="メールアドレス"
                required
                @input="$v.email.$touch()"
                @blur="$v.email.$touch()"
                @keyup.enter = "() => {if (!$v.email.$invalid) sendResetEmail()}"
                v-else
                outlined
              />
              </v-col>
              <v-row justify="end" class="col-11">
                <v-btn
                  @click="changePassword"
                  :disabled="$v.password.$invalid || $v.rePassword.$invalid || this.password !== this.rePassword"
                  v-if="$route.params.uid && $route.params.token"
                >
                  変更する
                </v-btn>
                <v-btn
                  @click="sendResetEmail"
                  :disabled="$v.email.$invalid"
                  v-else
                >
                  送信する
                </v-btn>
              </v-row>
            </v-row>
          </v-form>
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>

<script>
import {validationMixin} from 'vuelidate';
import {required, minLength, email} from 'vuelidate/lib/validators';

export default {
  name: "token",
  auth: false,

  mixins: [validationMixin],

  validations: {
    password: {required, minLength: minLength(8)},
    rePassword: {required, minLength: minLength(8)},
    email: {required, email},
  },

  head: {
    title: "パスワード変更",
  },

  data() {
    return {
      staled: false,
      password: "",
      rePassword: "",
      passwordError: "",
      show: false,
      reShow: false,
      email: ""
    }
  },

  computed: {
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
    emailErrors() {
      const errors = [];
      if (!this.$v.email.$dirty) return errors;
      if (!this.$v.email.email) errors.push("有効なメールアドレスを入力してください");
      if (!this.$v.email.required) errors.push("メールアドレスを入力してください");
      return errors;
    },
  },

  beforeCreate() {
    if (!!this.$route.params.uid ^ !!this.$route.params.token) this.$router.push("/");
  },

  methods: {
    changePassword() {
      this.$axios.$post("auth/users/reset_password_confirm/", {uid: this.$route.params.uid, token: this.$route.params.token, new_password: this.password, re_new_password: this.rePassword},
        {"headers": {
            "Content-Type": "application/json",
            "Authorization": ""
          }})
        .then(response => {
          this.$router.push("/");
          this.$toasted.success("パスワードを変更しました", {
            theme: "bubble",
            position: "top-center",
            duration: 3000,
          });
        })
        .catch(e => {
          console.log(e);
          if (e.response) {
            if (e.response.data.new_password !== undefined) {
              if (e.response.data.new_password[0] === "このパスワードは一般的すぎます。") this.passwordError = "このパスワードは簡単すぎます";
              else if (e.response.data.new_password[0] === "このパスワードは email と似すぎています。") this.passwordError = "このパスワードはメールアドレスと似すぎています";
              else if (e.response.data.new_password[0] === "このパスワードは username と似すぎています。") this.passwordError = "このパスワードはユーザーネームと似すぎています";
              else this.passwordError = e.response.data.new_password[0];
            }
          }
          this.staled = e.request.responseText === "{\"token\":[\"Invalid token for given user.\"]}"
          if (this.passwordError === "" && !this.staled) this.$toasted.error("パスワードの変更に失敗しました", {
            theme: "bubble",
            position: "top-center",
            duration: 3000,
          });
        });
    },
    sendResetEmail() {
      this.$axios.$post("auth/users/reset_password/", {email: this.email})
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
        })
    }
  }
};
</script>

<style scoped>

</style>
