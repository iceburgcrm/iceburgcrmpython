<script setup>
import BreezeButton from '@/Components/Button.vue';
import BreezeCheckbox from '@/Components/Checkbox.vue';
import BreezeGuestLayout from '@/Layouts/Guest.vue';
import BreezeInput from '@/Components/Input.vue';
import BreezeLabel from '@/Components/Label.vue';
import BreezeValidationErrors from '@/Components/ValidationErrors.vue';
import { Head, Link, useForm } from '@inertiajs/inertia-vue3';
import { computed, onMounted, ref } from 'vue';
import axios from 'axios';

const props = defineProps({
    canResetPassword: Boolean,
    status: String,
    auth: [Object, Array, null],
    errors: {
        type: Object,
        default: () => ({})
    },
    loginUrl: String,
    csrfToken: String,
});

const email = ref('');
const password = ref('');
const remember = ref(false);
const errors = ref({});



const submit = () => {
   
    axios.post(props.loginUrl, {
        email: email.value,
        password: password.value,
        remember: remember.value,
    }, {
        headers: {
            'X-CSRFToken': props.csrfToken  // Ensure CSRF token is sent in headers
        },
        withCredentials: true  // Important for cookies if sessions are used
    })
    .then(response => {
        password.value = '';
        if (response.data.login) {
            window.location.href = '/dashboard/';
        } else {
            errors.value = { error: response.data.error }; // Update the errors ref with the error message
        }
    })
    .catch(error => {
        if (error.response) {
            console.error("Error data:", error.response.data);
            errors.value = error.response.data.errors || { error: 'An error occurred during login' }; // Update the errors ref with validation errors or a default error message
        }
    });
};

</script>

<template>
    <BreezeGuestLayout  :auth="props.auth">
        <Head title="Log in" />


        <div v-if="status" class="mb-4 font-medium text-sm text-success-content">
            {{ status }}
        </div>
    
        {{$page.props.auth.system_settings.title ? $page.props.auth.system_settings.title : ''}}
        <form @submit.prevent="submit" class=" bg-base-200 text-base-content">
            <span class="mt-5 mb-5" v-if="errors.error">{{ errors.error }}</span>
            <div class="form-control">
                <label class="label">
                    <span class="label-text">Email</span>
                </label>
                <input type="text" placeholder="email" class="input input-bordered" v-model="email" required autofocus autocomplete="username" />
            </div>
            <div class="form-control">
                <label class="label">
                    <span class="label-text">Password</span>
                </label>

                <input type="password" placeholder="password" class="input input-bordered" v-model="password" required autocomplete="current-password" />
                    <label class="label">
                    <a v-if="canResetPassword" :href="route('password.request')" class="label-text-alt link link-hover">Forgot password?</a>
                </label>
            </div>

            <div class="form-control mt-6">
                <button class="btn btn-primary" type="submit">Login</button>

            </div>
            <!--
            <Link v-if="canRegister" :href="route('register')" class="ml-4 text-sm text-base-content underline">
                    Register
                </Link>
                -->



        </form>
    </BreezeGuestLayout>
</template>
