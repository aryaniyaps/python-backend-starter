import createJiti from 'jiti';
import { fileURLToPath } from 'node:url';
const jiti = createJiti(fileURLToPath(import.meta.url));

// Import env here to validate during build. Using jiti we can import .ts files :)
jiti('./lib/env');

/** @type {import('next').NextConfig} */
const nextConfig = {};

export default nextConfig;
