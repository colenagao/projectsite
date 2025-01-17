<template>
  <nav class="navbar" role="navigation" aria-label="main navigation">
  <div class="navbar-brand">
    <a class="navbar-item" href="/calendar">
      <img src="/img/cat.png" />
    </a>

    <a
      role="button"
      class="navbar-burger"
      aria-label="menu"
      aria-expanded="false"
      data-target="navbarBasicExample"
    >
      <span aria-hidden="true"></span>
      <span aria-hidden="true"></span>
      <span aria-hidden="true"></span>
    </a>
  </div>

  <div id="navbarBasicExample" class="navbar-menu">
    <div class="navbar-start">

      <a class="navbar-item" href="/project">Projects</a>
      
      <a class="navbar-item" href="https://github.com/colenagao" target="_blank" rel="noopener noreferrer"> Github </a>

      <a class="navbar-item" href="https://www.linkedin.com/in/cole-nagao-0abb9a165/" target="_blank" rel="noopener noreferrer"> LinkedIn </a>

      <a class="navbar-item" href="/about">About Me</a>

    </div>

    <div class="navbar-end">
      <div class="navbar-item">
        <div class="buttons">
          <div class="navbar-item">Logged in as </div>
          <a class="button is-danger" href="/logout">
            <strong>Log Out</strong>
          </a>
          <a class="button is-primary" href="/signup">
            <strong>Sign up</strong>
          </a>
          <a class="button is-light" href="/login"> Log in </a>
        </div>
      </div>
    </div>
  </div>
</nav>
</template>

<script>
export default {
  name: 'Navbar',
  data() {
    return {};
  },
};
</script>