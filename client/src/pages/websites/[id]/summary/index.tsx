import { useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { getWebsiteInfo } from "../../../../_api/websites";
import { Container, Title } from "../../../../_dsfr";

export default function WebsiteSummary() {
  const { id = "" } = useParams();
  const { data: website, isLoading, error } = useQuery({ queryKey: ['websites', id], queryFn: () => getWebsiteInfo(id) });
  if (isLoading || !website) return <p>Loading...</p>;
  if (error) return <p>error</p>;
  return (
    <Container fluid>
      <Title className="fr-mt-3w fr-mb-1w" look="h6">WebsiteSummary {website.url}</Title>
      <pre><code>{JSON.stringify(website, null, 2)}</code></pre>
    </Container>
  )
}