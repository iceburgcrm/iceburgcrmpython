<script setup>
import { VueElement, computed, ref, onMounted } from "vue";
import { Head, Link, useForm, usePage } from '@inertiajs/inertia-vue3';

const page = usePage();
const allProps = ref(page.props);  // Ensure it's reactive by wrapping in ref if necessary

const props = defineProps({
    terms: String,
    auth: [String, Object, null]
});
</script>

<template>
    <Head title="Terms of Service" />
    {{ terms }}
    <div class="font-sans text-gray-900 antialiased">
        <div class="pt-4 bg-gray-100">
            <div class="min-h-screen flex flex-col items-center pt-6 sm:pt-0">
                <div>
                    

                </div>

                <div class="w-full sm:max-w-2xl mt-6 p-6 bg-white shadow-md overflow-hidden sm:rounded-lg prose" >
                    <h1 class="mt-5 text-3xl text-center">Terms of Service</h1>

                    <p>Welcome to Iceburg CRM, a website that offers CRM hosting services. The following Terms of Service (&quot;TOS&quot;) apply to all users of the Iceburg CRM website and any related services, features, and functionalities that are available on or through this website.</p>

                <p>By accessing or using the Iceburg CRM website or any of its services, you agree to be bound by these terms and conditions. If you do not agree to these terms, please do not use the Iceburg CRM website.</p>

                <p> 1. Account Registration and Security To use our services, you must register for an account with Iceburg CRM. During the registration process, you must provide accurate and complete information. You are solely responsible for maintaining the confidentiality of your account information, including your password. You agree to notify us immediately of any unauthorized use of your account or any other breach of security.</p>

                <p> 2. Service Availability and Performance Iceburg CRM will make reasonable efforts to ensure that our services are available and perform properly. However, we do not guarantee that our services will be available at all times or that they will be error-free or uninterrupted. We may suspend or terminate our services at any time for any reason, without notice.</p>

                <p> 3. User Content and Conduct You are solely responsible for all content and materials that you upload, transmit, or otherwise make available through the Iceburg CRM website. You agree that you will not use our services to:</p>

                <p> &bull; Post, upload, transmit or otherwise make available any content that is illegal, harmful, threatening, abusive, harassing, tortious, defamatory, vulgar, obscene, libelous, invasive of another's privacy, hateful, or racially, ethnically or otherwise objectionable;  &bull; Impersonate any person or entity, or falsely state or otherwise misrepresent your affiliation with a person or entity;  &bull; Forge headers or otherwise manipulate identifiers in order to disguise the origin of any content transmitted through our services;  &bull; Post, upload, transmit, or otherwise make available any unsolicited or unauthorized advertising, promotional materials, spam, chain letters, pyramid schemes, or any other form of solicitation;  &bull; Violate any applicable laws or regulations.  1. Intellectual Property Rights All content, materials, and features available on the Iceburg CRM website, including but not limited to text, graphics, logos, images, and software, are owned by Iceburg CRM or its licensors and are protected by copyright, trademark, and other intellectual property laws. You are granted a limited, non-exclusive, non-transferable license to use the Iceburg CRM website and its services for your own personal or business use. You may not reproduce, modify, distribute, display, sell, or otherwise exploit any content, materials, or features available on the Iceburg CRM website without the prior written consent of Iceburg CRM.</p>

                <p> 1. Disclaimer of Warranties and Limitation of Liability The Iceburg CRM website and its services are provided &quot;as is&quot; without any warranties of any kind, whether express or implied, including but not limited to the implied warranties of merchantability, fitness for a particular purpose, and non-infringement. Iceburg CRM does not warrant that the Iceburg CRM website will be error-free, uninterrupted, or secure. In no event shall Iceburg CRM be liable for any direct, indirect, incidental, special, or consequential damages arising out of or in any way connected with the use or inability to use the Iceburg CRM website or its services, including but not limited to damages for loss of profits, business interruption, loss of data, or any other commercial damages or losses, even if Iceburg CRM has been advised of the possibility of such damages.</p>

                <p> 1. Indemnification You agree to indemnify and hold Iceburg CRM, its affiliates, officers, agents, and employees, harmless from any claim or demand, rob@phpdeveloper.ca continue</p>

                <p> including reasonable attorneys' fees, made by any third party due to or arising out of your use of the Iceburg CRM website or its services, your violation of these TOS, or your violation of any rights of another person or entity.</p>

                <p> 1. Termination Iceburg CRM may terminate your account and access to our services at any time, with or without cause, without prior notice, and without liability. Upon termination, you will no longer have access to your account, and any data or content stored on our servers may be deleted.</p>

                <p> 2. Changes to the TOS Iceburg CRM reserves the right to modify these TOS at any time, with or without notice. Your continued use of the Iceburg CRM website after any modifications to these TOS constitutes your acceptance of the modified terms.</p>

                <p> 3. Governing Law and Jurisdiction These TOS shall be governed by and construed in accordance with the laws of the United States and the state of California, without giving effect to any principles of conflicts of law. You agree to submit to the personal jurisdiction of the state and federal courts located in Los Angeles County, California.</p>

                <p> 4. Entire Agreement These TOS constitute the entire agreement between you and Iceburg CRM with respect to your use of the Iceburg CRM website and its services, and supersede all prior or contemporaneous communications and proposals, whether oral or written, between you and Iceburg CRM.</p>

                <p>If any provision of these TOS is found to be invalid or unenforceable, the remaining provisions shall remain in full force and effect.</p>

                <p>If you have any questions or concerns about these TOS or our services, please contact us at support@iceburgcrm.com.</p>
                <br>

                    <a href="/">Home</a><br>
                    <br>
                </div></div>
        </div>
    </div>
</template>
