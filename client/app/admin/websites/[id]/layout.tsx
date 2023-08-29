import { Badge, BadgeGroup, Container, Link, Nav, Text, Title } from "@/app/_dsfr"
import { Website } from "@/app/_types/websites"
type Props = {
  params: {
    id: string,
  },
  children: React.ReactNode,
}

export default async function WebsiteLayout({ params, children }: Props) {
  const currentPath = `/admin/websites/${params.id}`;
  const website: Website = await fetch(`${process.env.API_URL}/websites/${params.id}`, { cache: 'no-store' })
    .then(res => res.json()).catch(err => { });

  return (
    <Container as="main" className="fr-my-3w">
      <Link isSimple icon="arrow-left-line" iconPosition="left" href="/admin/websites">Retour aux sites web</Link>
      <Title className="fr-mt-3w fr-mb-1w" look="h6">{website.url}</Title>
      <Text className="fr-card__detail fr-mt-0 fr-mb-1w">
        Ajouté le {new Date(website.created_at).toLocaleDateString('FR-fr', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
      </Text>
      {(website?.tags?.length || 0 > 0)
        ? (
          <>
            <Text className="fr-card__detail fr-mt-0 fr-mb-1w">
              Appartient {website?.tags?.length || 1 > 1 ? "aux catégories:" : 'à la catégorie'}
            </Text>
            <BadgeGroup className="fr-mt-0 fr-mb-1w">
              {website?.tags?.map((tag) => <Badge noIcon variant="info" key={tag}>{tag}</Badge>)}
            </BadgeGroup>
          </>)
        : null}
      <Nav>
        <Link current={true} href={currentPath}>Résumé</Link>
        <Link current={false} href={`${currentPath}/crawls`}>Historique des crawls</Link>
        <Link current={false} href={`${currentPath}/configs`}>Configuration</Link>
      </Nav>
      {children}
    </Container>
  )
}