import Website from "./components/Website";
import { Container, Title } from "../../_dsfr";
import ManagmentBar from "./components/ManagmentBar";
import { Website as TWebsite } from "@/app/_types/websites";

export const dynamic = 'force-dynamic'

async function getData() {
  const websites: TWebsite[] = await fetch(`${process.env.API_URL}/websites`, { cache: 'no-store' })
    .then(res => res.json());
  return websites;
}

export default async function Websites() {
  const websites: TWebsite[] = await getData();
  return (
    <Container as="main" className="fr-my-6w">
      <Title look="h3">Sites web</Title>
      <hr className="fr-my-3w" />
      <ManagmentBar />
      <ul style={{ paddingInlineStart: 'unset' }} className='fr-mt-3w fr-mb-3w'>
        {websites.map(website => <Website key={website.url} website={website} />)}
      </ul>
    </Container>
  )
}