import { Navigate, Route, Routes } from 'react-router-dom';

import Layout from './pages/layout';
import WebsiteLayout from './pages/websites/[id]/layout';
import WebsiteCrawlHistory from './pages/websites/[id]/crawls';
import WebsiteConfigs from './pages/websites/[id]/configs';
import WebsiteList from './pages/websites';
import CreateWebsite from './pages/websites/create';
import Lighthouse from './pages/websites/[id]/crawls/[id]/lighthouse';

export default function Router() {
  return (
    <Routes>
      <Route path="/websites/:id/crawls/:crawlId/lighthouse" element={<Lighthouse />} />
      <Route element={<Layout />}>
        <Route path="/" element={<Navigate to="/websites" replace={true} />} />
        <Route path="/websites" element={<WebsiteList />} />
        <Route path="/websites/create" element={<CreateWebsite />} />
        <Route path="/websites/:id" element={<WebsiteLayout />}>
          <Route path="" element={<Navigate to="crawls" replace={true} />} />
          <Route path="crawls" element={<WebsiteCrawlHistory />} />
          <Route path="configs" element={<WebsiteConfigs />} />
        </Route>
      </Route>
    </Routes>
  );
}
