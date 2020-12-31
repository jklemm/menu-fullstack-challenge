import Dashboard from './views/dashboard.svelte'
import Pedidos from './views/pedidos.svelte'
import Clientes from './views/clientes.svelte'
import Layout from './views/layout.svelte'

const routes = [
  { name: '/', component: Dashboard, layout: Layout },
  { name: '/dashboard', component: Dashboard, layout: Layout },
  { name: '/pedidos', component: Pedidos, layout: Layout },
  { name: '/clientes', component: Clientes, layout: Layout },
]

export { routes }