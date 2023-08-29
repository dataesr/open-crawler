"use client"
import { useState } from "react";
import { Badge, BadgeGroup, Button, ButtonGroup, Link } from "../../../_dsfr"
import { Website as TWebsite } from "../../../_types/websites"

export default function Website({ website }: { website: TWebsite }) {
  return (
    <li className="fr-p-3w fr-mb-3w" style={{ border: '1px solid grey' }}>
      <div>
        <Link href={website.url}>{website.url}</Link>
        <Badge isSmall variant="success" className="fr-ml-2w">{website.processStatus}</Badge>
        <span className="fr-ml-2w">{new Date(website.lastCrawlAt).toLocaleString()}</span>
        <Link href={`/admin/websites/${website.id}`}>Voir le détail</Link>
      </div>
      {(website?.tags?.length || 0 > 0)
        ? <BadgeGroup>{website?.tags?.map((tag) => <Badge key={tag}>{tag}</Badge>)}</BadgeGroup>
        : null}
    </li>
  )
}