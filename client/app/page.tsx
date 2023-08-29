import { Container, Link } from "./_dsfr";

export default async function Home() {
  return (
    <Container as="main">
      <ul className='fr-mt-3w fr-mb-3w'>
        <li><Link href="/admin/websites">Admin</Link></li>
        <li><Link href="/public">Public</Link></li>
      </ul>
    </Container>
  )
}
