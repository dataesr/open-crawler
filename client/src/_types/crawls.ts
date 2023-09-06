export type Crawl = {
  id: string;
  website_id: string;
  status: string;
  url: string;
  depth: number;
  limit: number;
}

export type CrawlCount = {
  count: number;
}