import { Container, Title } from "@/app/_dsfr";
import { Crawl } from "@/app/_types/crawls";

type Props = { params: { id: string } }

async function getData(id: string) {
  const crawls: Crawl[] = await fetch(`${process.env.API_URL}/websites/${id}/crawls`, { cache: 'no-store' })
    .then(res => res.json())
    .catch(err => []);
  return crawls;
}

export default async function WebsiteCrawlHistory({ params }: Props) {
  const crawls: Crawl[] = await getData(params.id)
  return (
    <Container fluid>
      <Title className="fr-mt-3w fr-mb-1w" look="h6">Historique des crawls</Title>
      <pre><code>{JSON.stringify(crawls)}</code></pre>
    </Container>
  )
}