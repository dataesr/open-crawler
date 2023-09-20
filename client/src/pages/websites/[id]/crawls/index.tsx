import { Button, ButtonGroup, Col, Container, Row, Text, Title } from '../../../../_dsfr';
import { useParams } from 'react-router-dom';
import JobList from './components/job-list';
import SelectedJob from './components/selected-job';
import './styles/jobs.scss';
import { getCrawls } from '../../../../_api/websites';
import { useQuery } from '@tanstack/react-query';
import { useState } from 'react';
import { Crawl } from '../../../../_types/crawls';

export default function Crawls() {
  const { id = "" } = useParams();
  const [month, setMonth] = useState<number | null>(3);
  const { data, isLoading, error } = useQuery({ queryKey: ['websites', id, 'crawls', month], queryFn: () => getCrawls(id) });
  const [selected, setSelected] = useState<Crawl | null>(data?.data?.[0] || null);
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
          <ButtonGroup size="sm" isInlineFrom="sm">
            <Button variant={(month === 3) ? "secondary" : "text"} onClick={() => setMonth(3)}>3 derniers mois</Button>
            <Button variant={(month === 12) ? "secondary" : "text"} onClick={() => setMonth(12)}>Dernière année</Button>
            <Button variant={(month === 0) ? "secondary" : "text"} onClick={() => setMonth(0)}>Depuis le début</Button>
          </ButtonGroup>
        </div>
      </Row>
      <Row gutters>
        <Col xs={selected ? "7" : "12"}>
          {(count === 0) && (
            <Text bold>
              Aucune tâche
            </Text>
          )}
          {(crawls.length > 0) ? <JobList jobs={crawls} selected={selected} setSelected={setSelected} /> : null}
        </Col>
        {(selected) && (
          <Col xs="5">
            <SelectedJob job={selected} />
          </Col>
        )}
      </Row>
    </Container>
  );
}
