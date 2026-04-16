import React from 'react';
import { Helmet } from 'react-helmet-async';

export default function SEO({ title, description, url, image, type = 'website' }) {
  const siteName = 'VOX LOCAL — Your Personal AI Voice Agent';
  
  // Default values
  const pageTitle = title ? `${title} | ${siteName}` : siteName;
  const pageDescription = description || "Experience a privacy-first AI assistant that manages your files, reads your PDFs, and talks back to you in real-time—all without your data ever leaving your machine.";
  const pageUrl = url ? `https://voxlocal.ai${url}` : 'https://voxlocal.ai';
  // A default opengraph image path could go here
  const pageImage = image ? `https://voxlocal.ai${image}` : 'https://voxlocal.ai/favicon.png';

  return (
    <Helmet>
      {/* Standard metadata tags */}
      <title>{pageTitle}</title>
      <meta name='description' content={pageDescription} />
      
      {/* Open Graph tags for social media sharing */}
      <meta property='og:title' content={pageTitle} />
      <meta property='og:description' content={pageDescription} />
      <meta property='og:type' content={type} />
      <meta property='og:url' content={pageUrl} />
      <meta property='og:image' content={pageImage} />
      <meta property='og:site_name' content={siteName} />

      {/* Twitter tags */}
      <meta name='twitter:card' content='summary_large_image' />
      <meta name='twitter:title' content={pageTitle} />
      <meta name='twitter:description' content={pageDescription} />
      <meta name='twitter:image' content={pageImage} />
    </Helmet>
  );
}
