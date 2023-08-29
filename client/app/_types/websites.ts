type Metadata = {
  name: string;
  depth: number;
  enabled: boolean;
}

type Metadatas = {
  accessibility: Metadata;
  technologies_and_trackers: Metadata;
  responsiveness: Metadata;
  good_practices: Metadata;
  carbon_footprint: Metadata;
}

export type Website = {
  id: string;
  url: string;
  depth: number;
  limit: number;
  processStatus: string;
  tags?: string[];
  created_at: string;
  nextCrawlAt: string;
  lastCrawlAt: string;
  metadata?: Metadatas;
}