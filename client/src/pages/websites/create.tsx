import { useMutation } from "@tanstack/react-query";
import { useNavigate } from "react-router-dom";
import { Breadcrumb, Container, Notice, Link, Row, Title } from "../../_dsfr";
import WebsiteForm from "../../components/WebsiteForm";
import { WebsiteFormBody } from "../../_types/websites";
import { useState } from "react";
import { API_URL } from "../../_api/websites";

export default function CreateWebsite() {
  const [serverError, setServerError] = useState<string | null>(null);
  const navigate = useNavigate()
  const { isLoading: isMutating, mutate } = useMutation({
    mutationFn: (body: WebsiteFormBody) =>
      fetch(API_URL, { method: 'POST', body: JSON.stringify(body), headers: { 'Content-Type': 'application/json' } })
        .then((res) => res.json()),
    onSuccess: (res) => {
      navigate(`/websites/${res.id}`);
    },
    onError: () => setServerError('Une erreur est survenue lors de la création du site web.'),
  });
  return (
    <Container fluid className="fr-my-3w">
      <Breadcrumb>
        <Link href="/">Accueil</Link>
        <Link href="/websites">Sites web</Link>
        <Link>Ajouter un site web</Link>

      </Breadcrumb>
      <Row className="fr-my-3w">
        <Title look="h3">Ajouter un nouveau site web</Title>
      </Row>
      <WebsiteForm onSubmit={mutate} isLoading={isMutating} />
      {serverError && <Notice type="error">{serverError}</Notice>}
    </Container>
  )
}