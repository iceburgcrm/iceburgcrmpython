<script setup>
import { computed, onMounted } from 'vue';
import {Link, usePage} from '@inertiajs/inertia-vue3';

const props = defineProps({
    errors: {
     type: Object,
     default: () => ({})
   },
   auth: [Object, Array, null]
});


const errors = computed(() => props.errors);

const hasErrors = computed(() => Object.keys(errors.value).length > 0);
</script>

<template>
    <div v-if="hasErrors">
        <div class="font-medium text-red-600">Whoops! Something went wrong.</div>

        <ul class="mt-3 list-disc list-inside text-sm text-red-600">
            <li v-for="(error, key) in errors" :key="key">{{ error }}</li>
        </ul>
    </div>
</template>
