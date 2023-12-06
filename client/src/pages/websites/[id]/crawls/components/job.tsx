import { Link, Row } from '../../../../../_dsfr';
import { timeBetween, timeSince, timeTo } from '../utils/dates';
import { Crawl } from '../../../../../_types/crawls';
import SelectedJob from './selected-job';
import { useState } from 'react';
import StatusBadge from '../../../../../components/StatusBadge';

export default function Job({ job }: { job: Crawl }) {
  const [open, setOpen] = useState(false);
  const duration = timeBetween(new Date(job.started_at), new Date(job.finished_at));
  return (
    <>
      <div className="fr-p-1w" key={job.id}>
        <div className={`fr-card fr-card--shadow ${job.status}-border`}>
          <div className="fr-card__body fr-p-2w fr-enlarge-link">
            <Row>
              <Link className="card-button" onClick={() => setOpen((prev) => !prev)} />
              <div style={{ flexGrow: "1" }}>
                <span className="fr-m-0 fr-pr-1w fr-text--sm fr-text--bold fr-card__detail ">
                  {(['success', 'error', 'partial_error'].includes(job.status)) && (
                    <>
                      <span className="fr-icon--sm fr-mr-1w fr-icon-calendar-line" />
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
                      {timeSince(new Date(job.created_at))}
                    </>
                  )}
                </span>
              </div>
              <div style={{ display: "flex" }}>
                {(['success', 'error'].includes(job.status)) && (
                  <span className="fr-m-0 fr-mr-2w fr-pr-1w fr-text--sm fr-text--bold fr-card__detail ">
                    <span className="fr-icon--sm fr-mr-1w fr-icon-timer-line" />
                    {duration}
                  </span>
                )}
                <StatusBadge status={job.status} />
                <span className={`fr-ml-2w ${open ? 'fr-icon-arrow-down-s-line' : 'fr-icon-arrow-left-s-line'}`} />
              </div>
            </Row>
          </div>
          {open && (
            <div className="fr-card__footer fr-pt-0">
              <SelectedJob job={job} />
            </div>
          )
          }
        </div>
      </div>
    </>
  );
}

