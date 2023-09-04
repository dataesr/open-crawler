import { Outlet } from 'react-router-dom';
import { Container, Header, Link, Logo, Nav, Service } from '../_dsfr';

export default function Layout() {
  return (
    <>
      <Header>
        <Logo text="Ministère de | l'enseignement supérieur | et de la recherche" />
        <Service name="OpenCrawler" tagline="Client web pour OpenCrawler" />
        <Nav>
          <Link href="/websites">Sites webs</Link>
          <Link target="_blank" external={true} href="/flower">Tâches</Link>
        </Nav>
      </Header>
      <Container as="main" className="fr-my-3w">
        <Outlet />
      </Container>
    </>
  );
}
