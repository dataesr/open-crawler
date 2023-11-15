export type CrawlStatus = 'pending' | 'error' | 'success' | 'started' | 'partial_error';

export type MetadataResult = {
  task_id: string;
  started_at: string;
  finished_at: string;
  status: CrawlStatus;
}

export type Crawl = {
  id: string;
  website_id: string;
  status: CrawlStatus;
  url: string;
  depth: number;
  limit: number;
  created_at: string;
  started_at: string;
  finished_at: string;
  next_run_at: string;
  lighthouse: MetadataResult;
  technologies_and_trackers: MetadataResult;
  responsiveness: MetadataResult;
  carbon_footprint: MetadataResult;
  html_crawl: MetadataResult;
}

export type CrawlCount = {
  count: number;
}

export type CrawlList = {
  data: Crawl[];
  count: number;
}