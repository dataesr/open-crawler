import { Crawl } from "./crawls";

type Metadata = {
  depth: number;
  enabled: boolean;
}

export type WebsiteFormBody = {
  url: string;
  depth: number;
  limit: number;
  tags: string[];
  accessibility: Metadata;
  technologies_and_trackers: Metadata;
  responsiveness: Metadata;
  good_practices: Metadata;
  carbon_footprint: Metadata;
  headers: Record<string, string>;
}

export type Website = {
  id: string;
  status: string;
  tags: string[];
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