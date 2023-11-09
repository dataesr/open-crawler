import { Button, Col, Container, Row, Text, Title } from '../../../../_dsfr';
import { useParams } from 'react-router-dom';
import JobList from './components/job-list';
import './styles/jobs.scss';
import { API_URL, getCrawls } from '../../../../_api/websites';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

export default function Crawls() {
  const { id = "" } = useParams();
  const queryClient = useQueryClient();
  const { data, isLoading, error } = useQuery({ queryKey: ['websites', id, 'crawls'], queryFn: () => getCrawls(id), refetchOnWindowFocus: true, refetchInterval: 1000 * 15 });
  const { isLoading: isMutating, mutate: createNewCrawl } = useMutation({
    mutationFn: () =>
      fetch(`${API_URL}/${id}/crawls`, { method: 'POST', headers: { 'Content-Type': 'application/json' } }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['websites', id, 'crawls'] })
    },
    onError: () => { },
  });
  if (isLoading || !data) return <p>Loading...</p>;
  if (error) return <p>error</p>;
  const { data: crawls = [], count } = data;

  return (
    <Container fluid className="fr-my-6w">
      <Row>
        <div style={{ flexGrow: "1" }}>
          <Title look="h6">
            {count} crawl{count > 1 ? 's effectués' : ' effectué'}
          </Title>
        </div>
        <div>
          <Button disabled={isMutating || (crawls.filter((crawl) => ['pending', 'started'].includes(crawl.status)).length > 0)} variant="text" size="sm" iconPosition="left" icon="play-circle-line" onClick={() => createNewCrawl()}>
            Lancer un nouveau crawl
          </Button>
        </div>
      </Row>
      <Row gutters>
        <Col xs="12">
          {(count === 0) && (
            <Text bold>
              Aucune tâche
            </Text>
          )}
          {(crawls.length > 0) ? <JobList jobs={crawls} /> : null}
        </Col>
      </Row>
    </Container>
  );
}
