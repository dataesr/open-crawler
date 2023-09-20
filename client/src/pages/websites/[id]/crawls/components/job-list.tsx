import { Crawl } from '../../../../../_types/crawls';
import Job from './job';

export default function JobList({ jobs, selected, setSelected }: { jobs: Crawl[], selected: Crawl | null, setSelected: (crawl: Crawl) => void }) {
  return (
    <div className="job-list">
      {
        jobs.map((job) => (
          <Job key={job.id} job={job} selected={selected} setSelected={setSelected} />
        ))
      }
    </div>
  );
}
