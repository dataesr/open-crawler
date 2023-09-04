import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Link } from 'react-router-dom';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

import Router from './router';
import { DSFRConfig } from './_dsfr';
import './globals.scss';
import '@gouvfr/dsfr/dist/dsfr.min.css';
import '@gouvfr/dsfr/dist/utility/utility.min.css';

export const queryClient = new QueryClient();

const RouterLink = ({ href, replace, target, ...props }: { href: string, replace: boolean, target: string }) => {
  if (target === "_blank") return <a href={href} target={target} {...props} />
  return <Link to={href} replace={replace} {...props} />
}

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <DSFRConfig theme="light" lang="fr" routerComponent={RouterLink}>
      <BrowserRouter>
        <QueryClientProvider client={queryClient}>
          <ReactQueryDevtools />
          <Router />
        </QueryClientProvider>
      </BrowserRouter>
    </DSFRConfig>
  </React.StrictMode>,
);