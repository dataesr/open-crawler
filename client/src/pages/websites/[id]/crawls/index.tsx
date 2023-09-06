import { Container, Link, Title } from "../../../../_dsfr";
import { useQuery } from "@tanstack/react-query";
import { useParams } from "react-router-dom";
import { getCrawls, API_URL } from "../../../../_api/websites";
import { Crawl } from "../../../../_types/crawls";



export default function WebsiteCrawlHistory() {
  const { id = "" } = useParams();
  const { data: crawls, isLoading, error } = useQuery({ queryKey: ['websites',], queryFn: () => getCrawls(id) });
  if (isLoading || !crawls) return <p>Loading...</p>;
  if (error) return <p>error</p>;
  return (
    <Container fluid>
      <Title className="fr-mt-3w fr-mb-1w" look="h6">Historique des crawls</Title>
      {
        crawls.map((crawl: Crawl) => (
          <div key={crawl.id}>
            <Link href={`${API_URL}/${crawl.website_id}/crawls/${crawl.id}/files`} download>Download</Link>
            <pre><code>{JSON.stringify(crawl, null, 2)}</code></pre>
          </div>))
      }
    </Container >
  )
}