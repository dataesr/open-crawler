import { BadgeType } from '../../../../../_dsfr/components/Badge';
import { CrawlStatus } from '../../../../../_types/crawls';
type StatusLabel = 'En attente' | 'Echoué' | 'Réussi' | 'En cours' | 'Partiellement échoué';

const MAPPING: Record<CrawlStatus, [BadgeType, StatusLabel]> = {
  pending: ['info', 'En attente'],
  error: ['error', 'Echoué'],
  success: ['success', 'Réussi'],
  started: ['new', 'En cours'],
  partial_error: ['error', 'Partiellement échoué'],
};

export function getJobStatus(status: CrawlStatus): [BadgeType, StatusLabel] | [undefined, undefined] {
  return MAPPING[status] || [undefined, undefined];
}
