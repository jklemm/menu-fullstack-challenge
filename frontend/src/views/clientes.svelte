
<script>
  import { onMount } from "svelte";
  let clientes;

  onMount(async () => {
    await fetch(`http://localhost:8000/clientes`)
      .then(r => r.json())
      .then(data => {
        clientes = data;
      });
  })
</script>

<svelte:head>
    <title>Clientes</title>
</svelte:head>

<main role="main" class="col-md-9 ml-sm-auto col-lg-10 py-5 px-2">

  <div class="container-fluid">
    <h1>Clientes</h1>

    <table width="50%">
        <thead>
            <th>ID</th>
            <th>Nome Completo</th>
            <th>e-mail</th>
        </thead>
        <tbody>
        {#if clientes}
            {#each clientes as cliente }
                <tr>
                    <td>{cliente.id}</td>
                    <td>{cliente.primeiro_nome} {cliente.ultimo_nome}</td>
                    <td>{cliente.email}</td>
                </tr>
            {/each}
        {:else}
            <p class="loading">Carregando...</p>
        {/if}
        </tbody>
    </table>
  </div>

</main>
