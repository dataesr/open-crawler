import { API_URL } from '../../../../../_api/websites';
import { Badge, Link, Row } from '../../../../../_dsfr';
import { Crawl } from '../../../../../_types/crawls'
import { timeBetween } from '../utils/dates';
import { getJobStatus } from '../utils/status';
import Info from './selected-job-info';

// const metadatas = ['crawl', 'accessibility', 'responsiveness', 'technologies_and_tracker', 'best_practices', 'carbon_footprint', 'uploads']

export default function SelectedJob({ job }: { job: Crawl | null }) {
  if (!job) return null;
  const [badgeType, badgeLabel] = getJobStatus(job.status);
  return (
    <div className={`fr-card fr-card--xxs fr-card--horizontal fr-card--grey fr-card--no-border ${job.status}-border-right card-fit-content selected-div`}>
      <div className="fr-card__body">
        <div className="fr-card__content">
          <Info label="Id de la tâche" value={job.id} />
          <Info label="Status" value={<Badge isSmall variant={badgeType}>{badgeLabel}</Badge>} />
          {(job.status === 'error') && <Info label="Raison de l'échec" value={job.status} isCode />}
          <hr className="fr-my-2w fr-mx-1v" />
          {(job.status === 'started') && <Info label="Début de la tâche" value={job.started_at} />}
          {(['success', 'error'].includes(job.status)) && (
            <>
              <Info label="Début de la tâche" value={job.started_at} />
              <Info label="Fin de la tâche" value={job.finished_at || '-'} />
              <Info label="Durée de la tâche" value={timeBetween(new Date(job.started_at), new Date(job.finished_at))} />
            </>
          )}
          <hr className="fr-my-2w fr-mx-3v" />
          {['success', 'error', 'partial_error'].includes(job.status) && (<Row>
            <Link isSimple href={`${API_URL}/${job.website_id}/crawls/${job.id}/files`} download>Télécharger les fichiers</Link>
          </Row>)}
        </div>
      </div>
    </div>
  );
}

