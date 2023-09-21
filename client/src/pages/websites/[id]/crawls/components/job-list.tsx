import { Crawl } from '../../../../../_types/crawls';
import Job from './job';

export default function JobList({ jobs }: { jobs: Crawl[] }) {
  return (
    <div className="job-list">
      {
        jobs.map((job) => (
          <Job key={job.id} job={job} />
        ))
      }
    </div>
  );
}
