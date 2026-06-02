/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,

  allowedDevOrigins: [
    "172.25.145.245",
    "localhost",
    "127.0.0.1"
  ]
};

module.exports = nextConfig;