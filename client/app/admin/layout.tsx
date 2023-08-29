import { Header, Logo, Service, Link as DSFRLink, Nav } from '../_dsfr';

export default function AdminLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <>
      <Header>
        <Logo text="Ministère de | l'enseignement supérieur | et de la recherche" />
        <Service name="OpenCrawler" tagline="Client web pour OpenCrawler" />
        <Nav>
          <DSFRLink href="/admin">Dashboard</DSFRLink>
          <DSFRLink href="/admin/websites">Sites webs</DSFRLink>
          <DSFRLink target="_blank" external={true} href="/flower">Tâches</DSFRLink>
        </Nav>
      </Header>
      {children}
    </>
  )
}