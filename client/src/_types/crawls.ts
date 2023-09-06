export type Crawl = {
  id: string;
  website_id: string;
  status: string;
  url: string;
  depth: number;
  limit: number;
  created_at: string;
}

export type CrawlCount = {
  count: number;
}