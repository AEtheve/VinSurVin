import { createWebHistory, createRouter } from 'vue-router'

import MenuHeader from './components/MenuHeader.vue'
import Home from './components/Home.vue'
import Catalog from './components/Catalog.vue'
import Product from './components/Product.vue'
import Account from './components/Account.vue'
import CartProcess from './components/CartProcess.vue'
import LegalMentions from './components/LegalMentions.vue'
import SalesConditions from './components/SalesConditions.vue'
import OrderConfirmation from './components/OrderConfirmation.vue'

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
        {
            path: '/Product/:id',
            components:
            {
                default: MenuHeader,
                Product
            },
        },
        {
            path: '/cartprocess',
            components:
            {
                default: MenuHeader,
                CartProcess
            },
        },
        { 
            path: '/boutique', 
            name: 'Catalog', 
            component: Catalog 
        },
        {
            path: '/legalmentions',
            name : 'LegalMentions',
            components:
            {
                default: MenuHeader,
                LegalMentions
            },
        },
        {
            path: '/salesconditions',
            name : 'SalesConditions',
            components:
            {
                default: MenuHeader,
                SalesConditions
            },
        },
        {
            path: '/confirmation',
            name : 'confirmation',
            components:
            {
                default: MenuHeader,
                OrderConfirmation
            },
        },
    ],
});
export default router;