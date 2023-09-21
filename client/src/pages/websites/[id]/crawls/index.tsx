import { Col, Container, Row, Text, Title } from '../../../../_dsfr';
import { useParams } from 'react-router-dom';
import JobList from './components/job-list';
import './styles/jobs.scss';
import { getCrawls } from '../../../../_api/websites';
import { useQuery } from '@tanstack/react-query';

export default function Crawls() {
  const { id = "" } = useParams();
  const { data, isLoading, error } = useQuery({ queryKey: ['websites', id, 'crawls'], queryFn: () => getCrawls(id), refetchOnWindowFocus: false, staleTime: 1000 * 60 });
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
