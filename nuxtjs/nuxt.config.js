import colors from 'vuetify/es5/util/colors'

export default {
  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    htmlAttrs: {
      lang: 'ja',
      prefix: 'og: http://ogp.me/ns#'
    },
    titleTemplate: '%s - Study Review',
    title: '',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { name: 'format-detection', content: 'telephone=no' },
      { hid: 'description', name: 'description', content: '教育コンテンツの検索・レビューサイトです'},
      { hid: 'og:site_name', property: 'og:site_name', content: 'Study Review' },
      { hid: 'og:type', property: 'og:type', content: 'website' },
      { hid: 'og:url', property: 'og:url', content: 'https://studyreview.cogon-k.com' },
      { hid: 'og:title', property: 'og:title', content: 'Study Review' },
      { hid: 'og:description', property: 'og:description', content: '教育コンテンツの検索・レビューサイトです' },
      { hid: 'og:image', property: 'og:image', content: 'https://studyreview.cogon-k.com/img/icon.png' },
      { name: 'twitter:card', content: 'summary' }//　twitterの画像サイズ
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.png' }
    ],
    script: [
      { src: "lite-youtube-embed/lite-yt-embed.js" }
    ]
  },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: [
    "node_modules/lite-youtube-embed/src/lite-yt-embed.css"
  ],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: [
    { src: "~/plugins/star-rating.js", mode: "client", },
    { src: "~/plugins/tinymce.js", mode: "client" },
    { src: "~/plugins/vue-social-sharing.js", mode: "client" },
    { src: "~/plugins/scrollto.js" },
    { src: "~/plugins/sanitize.js" },
    { src: "~/plugins/vuedraggable.js" },
    { src: "~/plugins/vue-observe-visibility.js", mode: "client" },
  ],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
    // https://go.nuxtjs.dev/typescript
    '@nuxt/typescript-build',
    // https://go.nuxtjs.dev/vuetify
    '@nuxtjs/vuetify',
  ],

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
    // https://go.nuxtjs.dev/axios
    '@nuxtjs/axios',
    '@nuxtjs/auth-next',
    'cookie-universal-nuxt',
    '@nuxtjs/toast',
    'nuxt-fontawesome',
    '@nuxtjs/pwa',
    [
      'nuxt-compress',
      {
        gzip: {
          cache: true,
        },
        brotli: {
          threshold: 10240,
        },
      },
    ],
  ],

  // Axios module configuration: https://go.nuxtjs.dev/config-axios
  axios: {
    // Workaround to avoid enforcing hard-coded localhost:3000: https://github.com/nuxt-community/axios-module/issues/308
    baseURL: 'http://140.83.33.150/api/',
    //proxy: true
  },
  auth: {
    redirect: {
      login: '/login',
      logout: '/',
      callback: false,
      home: '/'
    },
    localStorage: false,
    strategies: {
      local: {
        scheme: 'refresh',
        endpoints: {
          login: { url: 'auth/jwt/create/', method: 'post', propertyName: 'access' },
          logout: false,
          refresh: { url: 'auth/jwt/refresh/', method: 'post' },
          user: { url: 'auth/users/me/', method: 'get', propertyName: false},
        },
        token:{
          property: 'access',
          data: 'access',
          maxAge: 60 * 5
        },
        refreshToken: {
          property: 'refresh',
          data: 'refresh',
          maxAge: 60 * 60 * 6
        },
        user: {
          property: false
        },
      }
    },
  },
  router: {
    middleware: ['auth']
  },
  fontawesome: {
    component: "fa",
    imports: [
      {
        set: "@fortawesome/free-solid-svg-icons",
        icons: ["faEnvelope",],
      },
      {
        set: "@fortawesome/free-brands-svg-icons",
        icons: ["faTwitter", "faLine", "faFacebookF"],
      },
    ],
  },

  // PWA module configuration: https://go.nuxtjs.dev/pwa
  pwa: {
    meta: {
      name: "Study Review"
    },
    icon: {
      source: '~/static/img/icon.png',
      fileName: 'icon.png'
    },
    manifest: {
      name: "Study Review",
      title: "Study Review",
      'og:title': 'Study Review',
      description: '教育コンテンツの検索・レビューサイトです',
      'og:description': '教育コンテンツの検索・レビューサイトです',
      lang: 'ja',
      theme_color: "#31afe3",
      background_color: "#bde0c0",
      display: "standalone",
      scope: "/",
      start_url: "/",
    },
  },

  // Vuetify module configuration: https://go.nuxtjs.dev/config-vuetify
  vuetify: {
    customVariables: ['~/assets/variables.scss'],
    theme: {
      //dark: false,
      themes: {
        dark: {
          primary: colors.blue.darken2,
          accent: colors.grey.darken3,
          secondary: colors.amber.darken3,
          info: colors.teal.lighten1,
          warning: colors.amber.base,
          error: colors.deepOrange.accent4,
          success: colors.green.accent3
        }
      },
      light: {
        primary: colors.blue.darken2,
        accent: colors.grey.darken3,
        secondary: colors.amber.darken3,
        info: colors.teal.lighten1,
        warning: colors.amber.base,
        error: colors.deepOrange.accent4,
        success: colors.green.accent3
      }
    }
  },
  publicRuntimeConfig: {
    TMCE_TOKEN: process.env.TMCE_TOKEN,
  },

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {
  }
}
