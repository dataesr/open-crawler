import { Link } from "..";

export default function PaginationItem({
  page,
  isActive,
  buildURL,
  aria,
}: { page: number, isActive?: boolean, buildURL: (page: number) => string, aria: string }) {
  const url = buildURL(page)
  return (
    <li>
      <Link
        aria-current={(isActive && 'page') || undefined}
        href={url}
        className="fr-pagination__link"
        aria-label={aria}
        title={aria}
      >
        {page}
      </Link>
    </li>
  );
}

