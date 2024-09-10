import { createWebHistory, createRouter } from 'vue-router'

import MenuHeader from './components/MenuHeader.vue'
import Home from './components/Home.vue'
import Catalog from './components/Catalog.vue'
import Account from './components/Account.vue'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            components:
            {
                default: MenuHeader,
                Home
            },
        },

        {
            path: '/boutique',
            components:
            {
                default: MenuHeader,
                Catalog
            },
        },

        {
            path: '/account',
            components:
            {
                default: MenuHeader,
                Account
            },
        },



    ],
});
export default router;