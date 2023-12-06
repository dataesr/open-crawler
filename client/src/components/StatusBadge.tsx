import { Badge, BadgeType } from '../_dsfr/components/Badge';
import { CrawlStatus } from '../_types/crawls';
type StatusLabel = 'En attente' | 'Echoué' | 'Réussi' | 'En cours' | 'Partiellement échoué';

const MAPPING: Record<CrawlStatus, [BadgeType, StatusLabel]> = {
  pending: ['info', 'En attente'],
  error: ['error', 'Echoué'],
  success: ['success', 'Réussi'],
  started: ['new', 'En cours'],
  partial_error: ['warning', 'Partiellement échoué'],
};

function getJobStatus(status: CrawlStatus | null | undefined): [BadgeType, StatusLabel] {
  return status ? MAPPING[status] : MAPPING.pending;
}

export default function StatusBadge({ status }: { status: CrawlStatus | null | undefined }) {
  const [type, label] = getJobStatus(status);
  return <Badge isSmall variant={type}>{label}</Badge>;
}