import { API_URL } from '../../../../../_api/websites';
import { Badge, Button, ButtonGroup, Col, Row, Text } from '../../../../../_dsfr';
import { Crawl, MetadataResult } from '../../../../../_types/crawls'
import { timeBetween } from '../utils/dates';
import { getJobStatus } from '../utils/status';

type Metadata = 'html_crawl' | 'lighthouse' | 'responsiveness' | 'technologies_and_trackers' | 'carbon_footprint';
const metadatas: Metadata[] = ['html_crawl', 'lighthouse', 'responsiveness', 'technologies_and_trackers', 'carbon_footprint']

const nameMap: { [key in Metadata]: string } = {
  html_crawl: 'Crawl',
  lighthouse: 'LightHouse',
  responsiveness: 'Responsive',
  technologies_and_trackers: 'Technologies',
  carbon_footprint: 'Empreinte carbone',
}

function downloadFiles(url: string) {
  const link = document.createElement('a');
  link.href = url;
  link.download = url.split('/').pop() || 'file';
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

function MetadataReport({ name, data }: { name: Metadata, data: MetadataResult }) {
  const [badgeType, badgeLabel] = data?.status ? getJobStatus(data.status) : [undefined, 'Désactivé'];
  const duration = data?.finished_at ? timeBetween(new Date(data.started_at), new Date(data.finished_at)) : null;
  return (
    <>
      <Text size="sm" className="fr-card__detail" bold>{nameMap[name]}</Text>
      <Badge isSmall variant={badgeType}>{badgeLabel}</Badge>
      {duration && (
        <Text size="sm" bold className="fr-mb-0 fr-card__detail ">
          <span className="fr-icon--sm fr-mr-1w fr-icon-timer-line" />
          {duration}
        </Text>
      )}
    </>
  );
}

export default function SelectedJob({ job }: { job: Crawl | null }) {
  if (!job) return null;
  return (
    <div className={"fr-card fr-card--horizontal fr-card--no-border"}>
      <div className="fr-card__body fr-p-2w">
        <Row horizontalAlign='center' gutters>
          {metadatas.map((metadata: Metadata) => (
            <Col className="metadata" key={metadata}>
              <MetadataReport name={metadata} data={job[metadata]} />
            </Col>
          ))}
        </Row>
        <hr className="fr-mt-2w fr-mx-3v" />
        {['success', 'error', 'partial_error'].includes(job.status) && (
          <Row horizontalAlign='right'>
            <ButtonGroup isInlineFrom='xs' size='sm'>
              <Button onClick={() => downloadFiles(`${API_URL}/${job.website_id}/crawls/${job.id}/files`)} size="sm" icon="download-line" variant="secondary" color="blue-ecume">Télécharger les fichiers</Button>
              <Button size="sm" icon="delete-line" variant="secondary" color="error">Supprimer le crawl</Button>
            </ButtonGroup>
          </Row>
        )}
      </div>
    </div>
  );
}

