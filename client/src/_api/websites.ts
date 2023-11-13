import { CrawlList } from "../_types/crawls";
import { Website, WebsiteFormBody, WebsiteList } from "../_types/websites";

export const API_URL = import.meta.env.VITE_API_URL ? `${import.meta.env.VITE_API_URL}/api/websites` : '/api/websites';

export async function getWebsites(search: string): Promise<WebsiteList> {
  return fetch(`${API_URL}${search}`).then((response) => {
    if (response.ok) return response.json();
    return { data: [], status: [], tags: [], count: 0};
  });
}

export async function getWebsiteInfo(id: string): Promise<Website | null> {
  return fetch(`${API_URL}/${id}`).then((response) => {
    if (response.ok) return response.json();
    return null;
  });
}

export async function getCrawls(id: string): Promise<CrawlList> {
  const crawls = await fetch(`${API_URL}/${id}/crawls?limit=50`)
    .then(res => res.json())
    .catch(() => ({ data: [], count: 0 }));
  return crawls;
}

export async function createWebsite(body: WebsiteFormBody): Promise<Website> {
  const newWebsite = await fetch(API_URL, { method: 'POST', body: JSON.stringify(body) })
    .then(res => res.json())
  return newWebsite;
}

export async function updateWebsite(id: string, body: WebsiteFormBody): Promise<Website> {
  const newWebsite = await fetch(`${import.meta.env.VITE_API_URL}/websites/${id}`, { method: 'PATCH', body: JSON.stringify(body) })
    .then(res => res.json())
  return newWebsite;
}
