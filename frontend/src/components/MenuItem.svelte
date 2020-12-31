<script>
  export let name = "";
  export let href = "";
  export let active = false;
</script>

<li class="nav-item">
  <a class="nav-link" href="{ href }" class:active>
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-home"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
    { name }
    {#if active}
      <span class="sr-only">(current)</span>
    {/if}
  </a>
</li>

<style>
  .active {
    color: #007bff;
  }

  .feather {
    width: 16px;
    height: 16px;
    vertical-align: text-bottom;
  }
</style>