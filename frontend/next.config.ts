import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    domains: [
      'localhost',
      'res.cloudinary.com', // For Cloudinary images
      'aiyos.ph',
      'api.aiyos.ph'
    ],
  },
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/api/:path*',
      },
    ];
  },
  experimental: {
    typedRoutes: true,
  },
};

export default nextConfig;