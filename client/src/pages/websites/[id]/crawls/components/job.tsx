import { Badge, Link, Row, Text } from '../../../../../_dsfr';
import classNames from 'classnames';
import { timeBetween, timeSince, timeTo } from '../utils/dates';
import { getJobStatus } from '../utils/status';
import { Crawl } from '../../../../../_types/crawls';

export default function Job({ job, selected, setSelected }: { job: Crawl, selected: Crawl | null, setSelected: (crawl: Crawl) => void }) {
  const [badgeType, badgeLabel] = getJobStatus(job.status);
  const duration = timeBetween(new Date(job.started_at), new Date(job.finished_at));
  const classname = classNames('job', { selected: job.id === selected?.id });
  return (
    <div className={classname} key={job.id}>
      <div className={`fr-card fr-card--horizontal fr-card--grey fr-enlarge-link fr-card--no-border ${job.status}-border`}>
        <div className="fr-card__body fr-p-2w">
          <Link className="card-button" onClick={() => setSelected(job)} />
          <Row>
            <div style={{ flexGrow: "1", display: "flex" }}>
              <Text className="fr-mb-0 fr-mr-2w" bold size="sm">{job.id}</Text>
              <Badge isSmall variant={badgeType}>{badgeLabel}</Badge>
            </div>
            <div>
              <span className="fr-m-0 fr-pr-1w fr-text--sm fr-text--bold fr-card__detail ">
                {(['success', 'error'].includes(job.status)) && (
                  <>
                    <span className="fr-icon--sm fr-mr-1w fr-icon-timer-line" />
                    {duration}
                    <span className="fr-icon--sm fr-ml-4w fr-mr-1w fr-icon-calendar-line" />
                    il y a
                    {' '}
                    {timeSince(new Date(job.finished_at))}
                  </>
                )}
                {(job.status === 'started') && (
                  <>
                    <span className="fr-icon--sm fr-mr-1w fr-icon-calendar-line" />
                    démarrée il y a
                    {' '}
                    {timeTo(new Date(job.started_at))}
                  </>
                )}
                {(job.status === 'pending') && (
                  <>
                    <span className="fr-icon--sm fr-mr-1w fr-icon-calendar-line" />
                    en attente depuis
                    {' '}
                    {timeSince(new Date(job.started_at))}
                  </>
                )}
              </span>
            </div>
          </Row>
        </div>
      </div>
    </div>
  );
}

