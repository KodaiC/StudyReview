<template>
  <v-main>
    <v-container>
      <v-row justify="center">
        <v-col>
          <h2 class="text-center ma-10">メールアドレス変更</h2>
          <h3 class="text-center" v-if="staled">
            トークンの期限が切れました<br>
            もう一度<NuxtLink to="mypage">マイページ</NuxtLink>から変更の手続きをやり直してください
          </h3>

          <v-form class="mt-10" v-if="!staled" @submit.prevent>
            <v-row justify="center">
              <v-col cols="11">
                <v-text-field
                  v-model="email"
                  :error-messages="emailErrors"
                  label="メールアドレス"
                  required
                  @input="() => {this.$v.email.$touch(); this.emailError = ''}"
                  @blur="() => {this.$v.email.$touch(); this.emailError = ''}"
                  @keyup.enter = "() => {if (!$v.$invalid) changeEmail()}"
                  outlined
                />
              </v-col>
              <v-row justify="end" class="col-11">
                <v-btn
                  @click="changeEmail"
                  :disabled="$v.$invalid"
                >
                  変更する
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
import {required, email} from 'vuelidate/lib/validators';

export default {
  name: "token",
  auth: false,

  mixins: [validationMixin],

  validations: {
    email: {required, email},
  },

  head: {
    title: "メールアドレス変更",
  },

  data() {
    return {
      staled: false,
      email: "",
      emailError: "",
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
  },

  beforeCreate() {
    if (!this.$route.params.uid || !this.$route.params.token) this.$router.push("/");
  },

  methods: {
    changeEmail() {
      this.$axios.$post("auth/users/reset_email_confirm/", {uid: this.$route.params.uid, token: this.$route.params.token, new_email: this.email},
      {"headers": {
          "Content-Type": "application/json",
          "Authorization": ""
        }})
      .then(response => {
        this.$router.push("/");
        this.$toasted.success("メールアドレスを変更しました", {
          theme: "bubble",
          position: "top-center",
          duration: 3000,
        });
      })
      .catch(e => {
        console.log(e);
        if (e.response) {
          if (e.response.data.new_email !== undefined) {
            if (e.response.data.new_email[0] === "この email を持った user が既に存在します。") this.emailError = "このメールアドレスは既に使われています";
            else this.emailError = e.response.data.new_email[0];
          }
        }
        this.staled = e.request.responseText === "{\"token\":[\"Invalid token for given user.\"]}"
        if (this.emailError === "" && !this.staled) this.$toasted.error("メールアドレスの変更に失敗しました", {
          theme: "bubble",
          position: "top-center",
          duration: 3000,
        });
      });
    }
  }
};
</script>

<style scoped>

</style>
