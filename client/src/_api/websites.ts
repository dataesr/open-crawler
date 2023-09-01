import { Crawl } from "../_types/crawls";
import { Website, WebsiteFormBody } from "../_types/websites";

const API_URL = `${import.meta.env.VITE_API_URL}/websites`

export async function getWebsites(): Promise<Website[]> {
  return fetch(API_URL).then((response) => {
    if (response.ok) return response.json();
    return [];
  });
}

export async function getWebsiteInfo(id: string): Promise<Website | null> {
  return fetch(`${API_URL}/${id}`).then((response) => {
    if (response.ok) return response.json();
    return null;
  });
}

export async function getCrawls(id: string): Promise<Crawl[]> {
  const crawls = await fetch(`${API_URL}/${id}/crawls`)
    .then(res => res.json())
    .catch(() => []);
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
