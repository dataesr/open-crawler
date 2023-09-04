import { useQuery } from '@tanstack/react-query';
import { Container, Title, Link, Badge, Breadcrumb, Text, Row, Button, Input } from '../../_dsfr';
import { Website } from '../../_types/websites';
import { getWebsites } from '../../_api/websites';

export default function WebsiteList() {
  const { data: websites, isLoading, error } = useQuery({ queryKey: ['websites'], queryFn: getWebsites });
  if (isLoading || !websites) return <p>Loading...</p>;
  if (error) return <p>error</p>;
  return (
    <Container fluid>
      <Breadcrumb>
        <Link href="/">Accueil</Link>
        <Link>Sites web</Link>
      </Breadcrumb>
      <Row className="fr-mt-3w fr-mb-1w">
        <Title look="h3">Sites web</Title>
      </Row>
      <Row>
        <Text className="fr-error-text fr-text--xs fr-mb-2w">
          Recherche, filtres et tri et pagination non fonctionnels actuellement
        </Text>
      </Row>
      <Row className="list-manager">
        <div className="grow">
          <Input disabled placeholder="Rechercher un site web" />
        </div>
        <div >
          <div className="fr-select-group">
            <select disabled className="fr-select" id="tag" name="tag">
              <option value="" selected disabled hidden>Tag</option>
              <option value="1">Option 1</option>
              <option value="2">Option 2</option>
              <option value="3">Option 3</option>
              <option value="4">Option 4</option>
            </select>
          </div>
        </div>
        <div >
          <div className="fr-select-group">
            <select disabled className="fr-select" id="status" name="status">
              <option value="" selected disabled hidden>Status</option>
              <option value="1">Option 1</option>
              <option value="2">Option 2</option>
              <option value="3">Option 3</option>
              <option value="4">Option 4</option>
            </select>
          </div>
        </div>
        <div >
          <div className="fr-select-group">
            <select disabled className="fr-select" id="sort" name="sort">
              <option value="" selected disabled hidden>Tri</option>
              <option value="1">Option 1</option>
              <option value="2">Option 2</option>
              <option value="3">Option 3</option>
              <option value="4">Option 4</option>
            </select>
          </div>
        </div>
        <div>
          <Button iconPosition="left" icon="add-line" color="success" href="/websites/create">Nouveau</Button>
        </div>
      </Row>
      <ul style={{ paddingInlineStart: 'unset', border: '1px solid var(--border-default-grey)', borderRadius: "8px" }} className='fr-my-3w'>
        {websites.map((website: Website) => (
          <li className="fr-enlarge-link fr-p-3w" style={{ borderBottom: '1px solid var(--border-default-grey)' }}>
            <Row verticalAlign="middle">
              <Link isSimple className="fr-mr-1w fr-text--heavy" size='lg' href={`/websites/${website.id}`}>{website.url}</Link>
              {(website?.tags?.length || 0 > 0)
                ? website?.tags?.map((tag) => <Badge className="fr-ml-1w" isSmall noIcon variant="new" key={tag}>{tag}</Badge>)
                : null}
            </Row>
            <Row>
              <Text className="fr-card__detail fr-my-0">
                Ajouté le {new Date(website.created_at).toLocaleDateString('FR-fr', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
              </Text>
            </Row>
            <Row>
              <Text className="fr-card__detail fr-my-0">
                Prochain crawl le {new Date(website.next_crawl_at).toLocaleDateString('FR-fr', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
              </Text>
            </Row>
          </li>
        ))}
      </ul>
    </Container >
  )
}