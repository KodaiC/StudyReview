<template>
  <v-app dark>
    <v-main>
      <v-container>
        <v-row justify="center">
          <v-col class="ma-5">
            <h1 v-if="error.statusCode === 404" class="text-center">
              {{ pageNotFound }}
            </h1>
            <h1 v-else class="text-center">
              {{ otherError }}
            </h1>
          </v-col>
        </v-row>
        <v-row justify="center">
          <NuxtLink to="/">
            トップページに戻る
          </NuxtLink>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: 'ErrorLayout',
  layout: 'error',
  auth: false,
  props: {
    error: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      pageNotFound: 'このページは存在しません',
      otherError: 'エラーが発生しました: ' + this.error.statusCode
    };
  },
  head() {
    const title = 'エラー';
    return {
      title
    };
  }
};
</script>

<style scoped>
h1 {
  font-size: 20px;
}
</style>
