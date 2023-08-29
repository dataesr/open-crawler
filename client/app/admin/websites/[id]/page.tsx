import { Badge, BadgeGroup, Container, Link, Nav, Text, Title } from "@/app/_dsfr"
import { Website } from "@/app/_types/websites"

export const dynamic = 'force-dynamic'

type Props = {
  params: {
    id: string,
  },
}

export default async function Page(props: Props) {
  const website: Website = await fetch(`${process.env.API_URL}/websites/${props.params.id}`, { cache: 'no-store' })
    .then(res => res.json()).catch(err => { });
  return (
    <Container fluid>
      <Title className="fr-mt-3w fr-mb-1w" look="h6">Résumé de {website.id}</Title>
    </Container>
  )
}