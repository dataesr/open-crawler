import { Container, Title } from "../../../../_dsfr";
import { useQuery } from "@tanstack/react-query";
import { useParams } from "react-router-dom";
import { getCrawls } from "../../../../_api/websites";


export default function WebsiteCrawlHistory() {
  const { id = "" } = useParams();
  const { data: crawls, isLoading, error } = useQuery({ queryKey: ['websites',], queryFn: () => getCrawls(id) });
  if (isLoading || !crawls) return <p>Loading...</p>;
  if (error) return <p>error</p>;
  return (
    <Container fluid>
      <Title className="fr-mt-3w fr-mb-1w" look="h6">Historique des crawls</Title>
      <pre><code>{JSON.stringify(crawls, null, 2)}</code></pre>
    </Container>
  )
}