export default function Info({ label, value, isCode = false }: { label: string, value: React.ReactNode | string | null, isCode?: boolean }) {
  return (
    <>
      <p className="fr-text--bold fr-text--sm fr-m-0">
        {label}
      </p>
      {(isCode)
        ? <pre className="fr-m-0 fr-text--sm fr-text--bold fr-card__detail fr-pb-1w job-code">{JSON.stringify(value, null, 2)}</pre>
        : <p className="fr-m-0 fr-text--sm fr-text--bold fr-card__detail fr-pb-1w">{value}</p>}
    </>
  );
}

