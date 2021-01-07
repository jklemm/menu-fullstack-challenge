
<script>
  import { onMount } from "svelte";
  let pedidos;

  onMount(async () => {
    await fetch(`http://localhost:8000/pedidos`)
      .then(r => r.json())
      .then(data => {
        pedidos = data;
      });
  })
</script>

<svelte:head>
    <title>Pedidos</title>
</svelte:head>

<main role="main" class="col-md-9 ml-sm-auto col-lg-10 py-5 px-2">

  <div class="container-fluid">
    <h1>Pedidos</h1>

    <table width="50%">
        <thead>
            <th>ID</th>
            <th>Data</th>
            <th>Cliente ID</th>
            <th>Valor</th>
        </thead>
        <tbody>
        {#if pedidos}
            {#each pedidos as pedido }
                <tr>
                    <td>{pedido.id}</td>
                    <td>{pedido.data}</td>
                    <td>{pedido.cliente_id}</td>
                    <td>{pedido.valor}</td>
                </tr>
            {/each}
        {:else}
            <p class="loading">Carregando...</p>
        {/if}
        </tbody>
    </table>
  </div>

</main>
