import { Outlet, useLocation, useParams } from "react-router-dom";
import { Badge, BadgeGroup, Breadcrumb, Container, Link, Nav, Text, Title } from "../../../_dsfr"
import { useQuery } from "@tanstack/react-query";
import { getWebsiteInfo } from "../../../_api/websites";


export default function WebsiteLayout() {
  const { id = "" } = useParams();
  const { pathname } = useLocation()
  const currentPath = `/websites/${id}`;
  const { data: website, isLoading, error } = useQuery({
    queryKey: ['websites', id],
    queryFn: () => getWebsiteInfo(id),
    staleTime: 1000 * 60 * 60,
    refetchOnWindowFocus: false,
    refetchOnMount: false,
    cacheTime: Infinity,
  });
  if (isLoading || !website) return <p>Loading...</p>;
  if (error) return <p>error</p>;

  return (
    <Container fluid>
      <Breadcrumb>
        <Link href="/websites">Accueil</Link>
        <Link>{website.url}</Link>
      </Breadcrumb>
      <Title className="fr-mt-3w fr-mb-1w" look="h4">{website.url}</Title>
      <Text className="fr-card__detail fr-my-0">
        Ajouté le {new Date(website.created_at).toLocaleDateString('FR-fr', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
      </Text>
      <Text className="fr-card__detail fr-my-0 fr-mb-3w">
        Prochain crawl le
        {' '}
        {new Date(website.next_crawl_at)
          .toLocaleDateString('FR-fr', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
      </Text>
      {(website?.tags?.length > 0)
        ? (
          <>
            <Text className="fr-card__detail fr-mt-0 fr-mb-1w">
              Appartient {(website.tags.length < 2) ? "à la catégorie:" : 'aux catégories:'}
            </Text>
            <BadgeGroup className="fr-mt-0 fr-mb-1w">
              {website?.tags?.map((tag) => <Badge noIcon variant="info" key={tag}>{tag}</Badge>)}
            </BadgeGroup>
          </>)
        : null}
      <Nav className="with-go-back">
        <Link isSimple href={"/websites"}>
          <span className="fr-icon-arrow-left-s-line fr-icon--sm fr-mr-1w" />
          Retour aux sites web
        </Link>
        <Link current={pathname.endsWith('crawls')} href={`${currentPath}/crawls`}>Historique des crawls</Link>
        <Link current={pathname.endsWith('configs')} href={`${currentPath}/configs`}>Configuration</Link>
      </Nav>
      <Outlet />
    </Container>
  )
}