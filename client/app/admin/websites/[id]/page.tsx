import { Badge, BadgeGroup, Container, Link, Nav, Text, Title } from "@/app/_dsfr"
import { Website } from "@/app/_types/websites"
type Props = {
  params: {
    id: string,
  },
}

export default async function Page(props: Props) {
  const website: Website = await fetch(`http://localhost:8080/websites/${props.params.id}`, { cache: 'no-store' })
    .then(res => res.json());
  return (
    <Container fluid>
      <Title className="fr-mt-3w fr-mb-1w" look="h6">Résumé</Title>
    </Container>
  )
}