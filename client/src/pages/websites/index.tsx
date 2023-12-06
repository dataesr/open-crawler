import { useQuery } from '@tanstack/react-query';
import {
  Container,
  Title,
  Link,
  Badge,
  Text,
  Row,
  Button,
  Input,
  InputChangeEvent,
  AnchorPagination,
} from '../../_dsfr';
import { Website } from '../../_types/websites';
import { getWebsites } from '../../_api/websites';
import { useSearchParams } from 'react-router-dom';
import { useCallback, useEffect, useState } from 'react';
import StatusBadge from '../../components/StatusBadge';

const PER_PAGE: number = 10

function getSkipAndLimitFromPage(page: number): [number, number] {
  return [(page - 1) * PER_PAGE, PER_PAGE];
}

export default function WebsiteList() {
  const [query, setQuery] = useState<string>('');
  const [searchParams, setSearchParams] = useSearchParams();
  const [skip, limit] = getSkipAndLimitFromPage(parseInt(searchParams.get('page') || "1", 10));

  const handleSearchParamChange = useCallback((key: string, value: string) => {
    if (value) searchParams.set(key, value); else searchParams.delete(key)
    setSearchParams(searchParams);
  }, [searchParams, setSearchParams])

  const clearFilters = useCallback(() => {
    setQuery('');
    setSearchParams({ query: '', tags: '', status: '', page: '1' });
  }, [setSearchParams])

  useEffect(() => {
    const delayDebounceFn = setTimeout(() => {
      handleSearchParamChange('query', query)
    }, 1000)

    return () => clearTimeout(delayDebounceFn)
  }, [handleSearchParamChange, query])

  const getQueryURL = () => {
    const queryURL = new URLSearchParams(searchParams);
    queryURL.set('skip', skip.toString());
    queryURL.set('limit', limit.toString());
    return queryURL.toString();
  }


  const { data, isLoading, error } = useQuery({
    queryKey: ['websites', getQueryURL()],
    queryFn: () => getWebsites(`?${getQueryURL()}`),
    refetchOnWindowFocus: false,
    refetchOnMount: false,
    staleTime: 1000 * 60,
  });
  if (isLoading || !data) return <p>Loading...</p>;
  if (error) return <p>error</p>;
  const { data: websites, count, tags, status } = data;
  return (
    <Container fluid>
      <Row className="fr-mt-3w fr-mb-1w">
        <Title look="h3">Sites web</Title>
      </Row>
      <Row className="list-manager">
        <div className="grow">
          <Input
            value={query}
            onChange={(e: InputChangeEvent) => setQuery(e.target.value)}
            disableAutoValidation
            defaultValue={searchParams.get('query') || ""}
            placeholder="Rechercher un site web"
          />
        </div>
        <div >
          <div className="fr-select-group">
            <select
              defaultValue={searchParams.get('tags') || ""}
              onChange={(e) => handleSearchParamChange('tags', e.target.value)}
              disabled={tags.length === 0}
              className="fr-select"
              id="tag"
              name="tag"
            >
              <option value="" hidden>Tag</option>
              {tags.map((tag: string) => <option value={tag}>{tag}</option>)}
            </select>
          </div>
        </div>
        <div >
          <div className="fr-select-group">
            <select
              defaultValue={searchParams.get('status') || ""}
              onChange={(e) => handleSearchParamChange('status', e.target.value)}
              disabled={status.length === 0}
              className="fr-select"
              id="status"
              name="status"
            >
              <option value="" disabled hidden>Status</option>
              {status.map((status: string) => <option value={status}>{status}</option>)}
            </select>
          </div>
        </div>
        <div >
          <div className="fr-select-group">
            <select
              defaultValue={searchParams.get('sort') || "-updated_at"}
              onChange={(e) => handleSearchParamChange('sort', e.target.value)}
              className="fr-select"
              id="sort"
              name="sort"
            >
              <option value="url">Ordre alphabetique</option>
              <option value="-updated_at">Date de modification</option>
            </select>
          </div>
        </div>
        <div>
          <Button iconPosition="left" icon="add-line" color="success" href="/websites/create">
            Nouveau
          </Button>
        </div>
      </Row>
      <Row verticalAlign='middle' className="fr-pl-1w fr-my-2w">
        <Text className="grow fr-text--sm fr-mb-0">
          <strong>{(count > 0) ? count : 'Aucun'}</strong> site{count > 1 && 's'} web
          {searchParams.get('query') && <span> pour la recherche <strong>{searchParams.get('query')}</strong></span>}
          {searchParams.get('tags') && <span> avec le tag <strong>{searchParams.get('tags')}</strong></span>}
          {searchParams.get('status') && <span> avec le status <strong>{searchParams.get('status')}</strong></span>}
          {searchParams.get('sort') && <span> triés par <strong>{searchParams.get('sort')}</strong></span>}
        </Text>
        {(searchParams.get('query') || searchParams.get('tags') || searchParams.get('status'))
          && <Button size="sm" iconPosition="left" icon="delete-line" variant="text" onClick={clearFilters}>Effacer les filtres</Button>}
      </Row>
      <ul style={{ paddingInlineStart: 'unset' }} className='fr-my-3w'>
        {websites.map((website: Website) => (
          <li className="fr-enlarge-link fr-p-3w" style={{ borderBottom: '1px solid var(--border-default-grey)' }}>
            <Row verticalAlign="middle">
              <Link isSimple className="fr-mr-1w fr-text--heavy" size='md' href={`/websites/${website.id}`}>{website.url}</Link>
              {(website?.tags?.length || 0 > 0)
                ? website?.tags?.map((tag) => <Badge className="fr-ml-1w" isSmall noIcon variant="new" key={tag}>{tag}</Badge>)
                : null}
            </Row>
            {website.last_crawl && (<Row>
              <Text className="fr-card__detail fr-my-0">
                Dernier crawl le
                {' '}
                {website.last_crawl?.created_at && new Date(website.last_crawl?.created_at)
                  .toLocaleDateString('FR-fr', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
              </Text>
            </Row>)}
            <StatusBadge status={website.last_crawl?.status} />
          </li>
        ))}
      </ul>
      <Row horizontalAlign='center'>
        <AnchorPagination
          currentPage={parseInt(searchParams.get('page') || "1", 10)}
          pageCount={(count > 0) ? ((count % limit) > 0) ? Math.floor(count / limit) + 1 : Math.floor(count / limit) : 1}
          buildURL={(page) => {
            const params = new URLSearchParams(searchParams)
            params.set('page', page.toString());
            return `/websites?${params.toString()}`;
          }}
        />
      </Row>
    </Container >
  )
}