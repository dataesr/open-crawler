// import '@gouvfr/dsfr/dist/dsfr.min.css';
// import '@gouvfr/dsfr/dist/utility/utility.min.css';
import './globals.css';
import Script from 'next/script';
import Link from 'next/link';
import { DSFRConfig } from './_dsfr';

export const metadata = {
  title: 'OpenCrawler',
  description: 'Client web pour OpenCrawler',
  viewport: 'width=device-width, initial-scale=1, shrink-to-fit=no',
  charset: 'utf-8',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="fr">
      <body>
        <DSFRConfig theme="light" lang="fr" routerComponent={Link}>
          {children}
        </DSFRConfig>
        <Script src="/dsfr.module.min.js" strategy='afterInteractive' />
        <Script src="/dsfr.nomodule.min.js" noModule strategy='afterInteractive' />
      </body>
    </html>
  )
}
