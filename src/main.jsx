import { createApp, h } from "vue";
import { createInertiaApp } from "@inertiajs/vue3";
import "vite/modulepreload-polyfill";
import axios from 'axios';
import "./index.css";
import "./assets/css/app.css";

axios.defaults.headers.common['X-CSRFToken'] = getCookie('csrftoken');

function getCookie(name) {
    let value = `; ${document.cookie}`;
    let parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}


createInertiaApp({
  resolve: (name) => {
    const pages = import.meta.glob("./Pages/**/*.vue", { eager: true });
    return pages[`./Pages/${name}.vue`];
  },
  setup({ el, App, props, plugin }) {
    const app = createApp({ render: () => h(App, props) });

    app.use(plugin);

    app.mixin({
      mounted() {
        if (this.$page && this.$page.props && this.$page.props.theme) {
          document.documentElement.setAttribute('data-theme', this.$page.props.auth.system_settings.theme);
        } 
      },
      watch: {
        '$page.props.auth.system_settings.theme'(newTheme) {
          if (newTheme) {
            document.documentElement.setAttribute('data-theme', newTheme);
          }
        }
      }
    });

    app.mount(el);
  },
});
