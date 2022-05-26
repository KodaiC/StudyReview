<template>
  <v-app>
    <v-main>
      <v-container>
        <v-form>
          <v-row justify="center">
            <v-col cols="12" md="8">
              <v-card>
                <v-container>
                  <v-row justify="center">
                    <h2 class="ma-5">ログイン</h2>
                    <v-col cols="11">
                      <v-text-field
                        v-model="email"
                        :error-messages="emailErrors"
                        label="メールアドレス"
                        @input="$v.email.$touch()"
                        @blur="$v.email.$touch()"
                        outlined
                      />
                    </v-col>
                    <v-col cols="11">
                      <v-text-field
                        v-model="password"
                        :error-messages="passwordErrors"
                        :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
                        :type="show ? 'text' : 'password'"
                        label="パスワード"
                        @input="$v.password.$touch()"
                        @blur="$v.password.$touch()"
                        @click:append="show = !show"
                        @keyup.enter="() => {if (!$v.invalid) login()}"
                        outlined
                      />
                      <NuxtLink to="reset/password">パスワードを忘れてしまった場合</NuxtLink>
                    </v-col>
                  </v-row>
                  <v-row justify="space-between" align="center" class="ml-0">
                    <NuxtLink to="/signup" class="ml-4 ml-md-8"><h4>新規アカウント登録</h4></NuxtLink>
                    <v-btn :disabled="$v.$invalid" class="mr-6 mr-md-12 my-10" @click="login">
                      ログイン
                    </v-btn>
                  </v-row>
                </v-container>
              </v-card>
            </v-col>
          </v-row>
        </v-form>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import {validationMixin} from 'vuelidate';
import {required, email, minLength} from 'vuelidate/lib/validators';

export default {
  mixins: [validationMixin],

  validations: {
    email: {required, email},
    password: {required, minLength: minLength(8),},
  },

  head: {
    title: "ログイン",
  },

  data() {
    return {
      password: "",
      email: "",
      show: false,
    };
  },

  computed: {
    emailErrors() {
      const errors = [];
      if (!this.$v.email.$dirty) return errors;
      if (!this.$v.email.email) errors.push("有効なメールアドレスを入力してください");
      if (!this.$v.email.required) errors.push("メールアドレスを入力してください");
      return errors;
    },
    passwordErrors() {
      const errors = [];
      if (!this.$v.password.$dirty) return errors;
      if (!this.$v.password.minLength) errors.push("パスワードは8文字以上です");
      if (!this.$v.password.required) errors.push("パスワードを入力してください");
      return errors;
    }
  },

  methods: {
    async login() {
      await this.$auth.loginWith('local', {
        data: {
          email: this.email,
          password: this.password
        }
      })
        .then(response => {
          this.$toasted.success("ログインしました", {
            theme: "bubble",
            position: "top-center",
            duration: 3000,
          });
          return response;
        })
        .catch(error => {
          this.$toasted.error("メールアドレスかパスワードが間違っています", {
            theme: "bubble",
            position: "top-center",
            duration: 3000,
          });
          return error;
        });
    }
  }
};
</script>
