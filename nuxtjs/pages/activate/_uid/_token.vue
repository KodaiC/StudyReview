<template>
  <v-main>
    <v-container>
      <v-row justify="center">
        <v-col>
          <h2 class="text-center ma-10">アカウント アクティベーション</h2>
          <h3 class="text-center" v-if="errorCode !== null && !staled">エラーが発生しました: {{ errorCode }}</h3>
          <h3 class="text-center" v-if="staled">トークンの期限が切れました</h3>

          <v-form class="mt-10" v-if="staled || (!$route.params.uid && !$route.params.token)" @submit.prevent>
            <v-row justify="center">
              <v-col cols="11">
                <v-text-field
                  v-model="email"
                  :error-messages="emailErrors"
                  label="メールアドレス"
                  required
                  @input="$v.email.$touch()"
                  @blur="$v.email.$touch()"
                  @keyup.enter = "() => {if (!$v.$invalid) resend()}"
                  outlined
                />
              </v-col>
              <v-row justify="end" class="col-11">
                <v-btn
                  @click="resend"
                  :disabled="$v.$invalid"
                >
                  再送する
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
    title: "アカウントアクティベーション",
  },

  data() {
    return {
      errorCode: null,
      activated: false,
      staled: false,
      email: ""
    }
  },

  computed: {
    emailErrors() {
      const errors = [];
      if (!this.$v.email.$dirty) return errors;
      if (!this.$v.email.email) errors.push("有効なメールアドレスを入力してください");
      if (!this.$v.email.required) errors.push("メールアドレスを入力してください");
      return errors;
    },
  },

  async mounted() {
    if (!!this.$route.params.uid && !!this.$route.params.token) {
      await this.$axios.$post("auth/users/activation/", {"uid": this.$route.params.uid, "token": this.$route.params.token},
        {"headers": {
          "Content-Type": "application/json",
          "Authorization": ""
        }})
        .then(response => {
          this.activated = true;
        })
        .catch(e => {
          console.log(e);
          if (e.response) {
            this.errorCode = e.response.status;
            this.staled = e.response.data.detail === "Stale token for given user.";
          }
          else {
            this.errorCode = "-1";
            this.staled = e.message === "Stale token for given user.";
          }
        });
    }

    if (this.errorCode === null && !(!this.$route.params.uid && !this.$route.params.token)) {
      await this.$router.push("/");
      if (this.activated) this.$toasted.success("アカウントを有効化しました", {
        theme: "bubble",
        position: "top-center",
        duration: 3000,
      });
    }
  },

  methods: {
    resend() {
      this.$axios.$post("auth/users/resend_activation/", {email: this.email},
        {"headers": {
            "Content-Type": "application/json",
            "Authorization": ""
          }});

      this.$toasted.success("確認メールを再送しました", {
        theme: "bubble",
        position: "top-center",
        duration: 3000,
      });
    }
  }
};
</script>

<style scoped>

</style>
