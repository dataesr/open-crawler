import { API_URL } from "../_api/websites";
import { Badge, Link, Row, Text } from "../_dsfr";
import { Crawl } from "../_types/crawls";

export default function CrawlItem({ crawl }: { crawl: Crawl }) {
  return (
    <li key={crawl.id} className="fr-pb-3w">
      <Row>
        <Text className="fr-mb-0" bold size='lg'>
          {new Date(crawl.created_at).toLocaleDateString('FR-fr', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
          <Text as="span">
            {' '}
            à
            {' '}
            {new Date(crawl.created_at).toLocaleTimeString('FR-fr', { hour: '2-digit', minute: '2-digit' })}
          </Text>
        </Text>
      </Row>
      <Row verticalAlign="middle">
        <Text className="fr-my-0">
          Status du crawl:
        </Text>
        <Badge className="fr-ml-1w" isSmall noIcon variant="new">{crawl.status}</Badge>
      </Row>
      <Row>
        <Link isSimple href={`${API_URL}/${crawl.website_id}/crawls/${crawl.id}/files`} download>Télécharger les fichiers</Link>
      </Row>
    </li>
  )
}