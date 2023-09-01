import { useMutation, useQuery } from "@tanstack/react-query";
import { useParams } from "react-router-dom";
import { getWebsiteInfo } from "../../../../_api/websites";
import { Container, Notice, Title } from "../../../../_dsfr";
import WebsiteForm from "../../../../components/WebsiteForm";
import { WebsiteFormBody } from "../../../../_types/websites";
import { useState } from "react";
import { queryClient } from "../../../../main";

export default function WebsiteConfigs() {
  const { id = "" } = useParams();
  const [serverError, setServerError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const { data: website, isLoading, error } = useQuery({ queryKey: ['websites', id], queryFn: () => getWebsiteInfo(id) });
  const { isLoading: isMutating, mutate } = useMutation({
    mutationFn: (body: WebsiteFormBody) =>
      fetch(`${import.meta.env.VITE_API_URL}/websites/${id}`, { method: 'PATCH', body: JSON.stringify(body), headers: { 'Content-Type': 'application/json' } }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['posts', id, 'comments'] })
      setSuccess('Vos modifications ont été enregistrées.')
    },
    onError: () => setServerError('Une erreur est survenue lors de la mise à jour du site web.'),
  });
  if (isLoading || !website) return <p>Loading...</p>;
  if (error) return <p>error</p>;
  const initialFormValues = website as WebsiteFormBody;
  return (
    <Container fluid className="fr-my-6w">
      <Title look="h5">Modifier la configuration de crawl</Title>
      <WebsiteForm initialForm={initialFormValues} onSubmit={mutate} create={false} isLoading={isMutating} />
      {serverError && <Notice type="error">{serverError}</Notice>}
      {success && <Notice type="success">{success}</Notice>}
    </Container>
  )
}