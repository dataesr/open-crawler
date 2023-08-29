"use client"
import { useRouter } from "next/navigation";
import { Button, Col, Row, SearchBar } from "../../../_dsfr"

export default function ManagmentBar() {
  const router = useRouter();
  return (
    <Row horitontalAlign="right">
      <Col xs={6} md={4}>
        <SearchBar placeholder="Rechercher un site web" onSearch={() => { }} className="fr-mb-3w" />
      </Col>
      <Col xs={4} offsetXs={2} md={3} offsetMd={5}>
        <Button icon="add-circle-line" onClick={() => router.push('/admin/websites/new')}>Ajouter un site web</Button>
      </Col>
    </Row>
  )
}