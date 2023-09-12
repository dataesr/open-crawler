import classNames from 'classnames';
import { getSurrendingLeft, getSurrendingRight } from './helpers';
import PaginationItem from './PaginationItem';
import { Link } from '..';

type PaginationProps = {
  pageCount: number,
  currentPage: number,
  buildURL: (page: number) => string,
  surrendingPages?: number,
}

export function AnchorPagination({
  pageCount,
  currentPage,
  buildURL,
  surrendingPages = 2,
}: PaginationProps) {
  const surrendingLeft = getSurrendingLeft(currentPage, surrendingPages);
  const surrendingRight = getSurrendingRight(currentPage, surrendingPages, pageCount);
  const buttonLabels = {
    navigationAria: 'Pagination navigation',
    currentAria: 'page',
    pageAria: (page: number): string => `Page ${page}`,
    prevLabel: 'Précédente',
    nextLabel: 'Suivante',
    prevAria: 'Page précédente',
    nextAria: 'Page suivante',
    firstAria: 'Première page',
    lastAria: 'Dernière Page',
  }
  const {
    navigationAria, prevLabel, nextLabel, prevAria,
    nextAria, firstAria, lastAria, currentAria, pageAria,
  } = buttonLabels;

  const getItem = (index: number, aria: string, icon: string | undefined = undefined, label: string | undefined = undefined): React.ReactNode => {
    const url = buildURL(index);
    return (
      <Link
        href={url}
        className={classNames({ [`fr-pagination__link--${icon}`]: aria }, 'fr-pagination__link')}
        aria-label={aria}
        title={aria}
      >
        {label}
      </Link>
    );
  };

  return (
    <nav
      className="fr-pagination"
      aria-label={navigationAria}
      role="navigation"
    >
      <ul className="fr-pagination__list">
        <li>
          {getItem(1, firstAria, 'first')}
        </li>
        <li>
          {getItem((currentPage - 1 > 0) ? (currentPage - 1) : 1, prevAria, 'prev', prevLabel)}
        </li>
        <PaginationItem
          page={1}
          isActive={currentPage === 1}
          buildURL={buildURL}
          aria={pageAria(1)}
        />
        {surrendingLeft.hasEllipsis && (
          <li>…</li>)}
        {surrendingLeft.pages.map((p) => (
          <PaginationItem
            key={p}
            page={p}
            buildURL={buildURL}
            aria={pageAria(p)}
          />
        ))}
        {((currentPage !== 1) && (currentPage !== pageCount)) && (
          <PaginationItem
            page={currentPage}
            buildURL={buildURL}
            isActive
            aria={currentAria}
          />
        )}
        {surrendingRight.pages.map((p) => (
          <PaginationItem
            key={p}
            page={p}
            buildURL={buildURL}
            aria={pageAria(p)}
          />
        ))}
        {surrendingRight.hasEllipsis && (
          <li>…</li>)}
        {(pageCount !== 1) && (
          <PaginationItem
            aria={pageAria(pageCount)}
            aria-current={(currentPage === pageCount && 'page') || undefined}
            isActive={currentPage === pageCount}
            page={pageCount}
            buildURL={buildURL}
          />
        )}
        <li>
          {getItem((currentPage + 1 < pageCount) ? currentPage + 1 : pageCount, nextAria, 'next', nextLabel)}
        </li>
        <li>
          {getItem(pageCount, lastAria, 'last')}
        </li>
      </ul>
    </nav>
  );
}
