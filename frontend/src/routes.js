import Dashboard from './views/dashboard.svelte'
import Pedidos from './views/pedidos.svelte'
import Clientes from './views/clientes.svelte'

const routes = [
  { name: '/', component: Dashboard },
  { name: '/dashboard', component: Dashboard },
  { name: '/pedidos', component: Pedidos },
  { name: '/clientes', component: Clientes },
]

export { routes }