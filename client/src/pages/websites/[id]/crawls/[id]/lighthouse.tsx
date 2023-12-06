import { useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import ReportViewer from 'react-lighthouse-viewer';
import { getCrawlMetadataFile } from "../../../../../_api/websites";

export default function Lighthouse() {
  const { id = "", crawlId = "" } = useParams<{ id: string, crawlId: string }>();
  const { data, isLoading, error } = useQuery({
    queryKey: ['lighthouse', id, crawlId],
    queryFn: () => getCrawlMetadataFile(id, crawlId, 'lighthouse'),
    refetchOnWindowFocus: true,
    refetchInterval: 1000 * 15
  });
  if (isLoading || !data) return <p>Loading...</p>;
  if (error) return <p>error</p>;
  const report = data?.[Object.keys(data)?.[0]];
  return <ReportViewer json={report} />
}