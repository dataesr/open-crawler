import { Crawl, CrawlStatus } from "./crawls";

type Metadata = {
  depth: number;
  enabled: boolean;
}

export type WebsiteFormBody = {
  url: string;
  depth: number;
  limit: number;
  tags: string[];
  identifiers: string[];
  lighthouse: Metadata;
  technologies_and_trackers: Metadata;
  carbon_footprint: Metadata;
  headers: Record<string, string>;
}

export type Website = {
  id: string;
  status: CrawlStatus;
  tags: string[];
  identifiers: string[];
  created_at: string;
  updated_at: string;
  next_crawl_at: string;
  last_crawl: Crawl | null;
} & WebsiteFormBody

export type WebsiteList = {
  data: Website[];
  status: string[];
  tags: string[];
  count: number;
}