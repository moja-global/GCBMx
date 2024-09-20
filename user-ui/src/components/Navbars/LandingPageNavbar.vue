<template>
  <div>
    <div class="nav-menu">
      <div class="nav-content" :class="showMenu ? 'open-menu' : 'closed-menu'">
        <NavbarComponent>
          <router-link to="/" class="navbar-logo">
            <img
              src="https://community.moja.global/img/logo-light.png"
              alt="Logo"
              class="logo-img"
            />
          </router-link>
          <ul class="menu-list">
             <!-- New menu options -->
             <li>
              <a :href="`${baseUrl}/gcbm/`" style="color: white;">GCBM</a>
            </li>
             <li>
              <a :href="`${baseUrl}/flint/configurations/point`" style="color: white;">Point</a>
            </li>
            <li>
              <a :href="`${baseUrl}/flint/configurations/rothc`" style="color: white;">RothC</a>
            </li>
            <li>
              <a
                href="https://docs.moja.global/en/master/"
                style="color: white;"
                target="_blank"
                rel="noreferrer noopener"
              >Documentation</a>
            </li>
            <li>
              <a
                href="mailto:info@moja.global"
                style="color: white;"
                target="_blank"
                rel="noreferrer noopener"
              >Contact Us</a>
            </li>
            <li>
              <a
                href="https://github.com/moja-global/FLINT-UI"
                style="color: white;"
                target="_blank"
                rel="noreferrer noopener"
              >GitHub</a>
            </li>
          </ul>
        </NavbarComponent>
      </div>
    </div>
  </div>
</template>


<script>
import { NavbarComponent } from '@moja-global/mojaglobal-ui'
import { ref } from 'vue'

export default {
  name: 'LandingPageNavbar',
  components: {
    NavbarComponent
  },
  setup() {
    const showMenu = ref(false)
    const baseUrl = process.env.VUE_APP_BASE_URL || '';

    return { showMenu, baseUrl }
  }
}
</script>

<style lang="scss" scoped>
.nav-menu {
  display: flex;
  justify-content: flex-start; /* Align menu to the right */
  padding: 0 20px; /* Add some padding */
}

.nav-content {
  display: flex;
  flex-direction: row;
  align-items: center;
}

.menu-list {
  display: flex;
  flex-direction: row;
  list-style: none;
  padding: 0;
  margin: 0;
}

.menu-list li {
  margin-right: 20px; /* Add spacing between menu items */
}

.menu-list a {
  text-decoration: none;
  padding-left: 1%;
}

/* Mobile responsiveness */
@media screen and (max-width: 768px) {
  .nav-menu {
    padding-top: 0;
    position: absolute;
    width: 100%;
    right: 0; /* Align to the right */
  }

  .open-menu {
    opacity: 1;
    height: 100px; /* Adjust height as needed */
    background: #333; /* Background color for the menu */
  }

  .closed-menu {
    opacity: 0;
    height: 0;
    padding: 0;
  }

  .nav-content {
    flex-direction: column;
    z-index: 100;
    position: relative;
  }

  .menu-list {
    flex-direction: column;
  }

  .menu-list li {
    margin-left: 0; /* Reset margin for mobile */
    margin-bottom: 10px; /* Space between items */
  }
}
</style>