import { Header, Logo, Service } from '../_dsfr';

export default function PublicLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <>
      <Header>
        <Logo text="Ministère de | l'enseignement supérieur | et de la recherche" />
        <Service name="OpenCrawler" tagline="Client web pour OpenCrawler" />
      </Header>
      {children}
    </>
  )
}
