import { cloneElement, isValidElement, useId } from 'react';
import { getChildrenOfType } from "../../utils/children"
import { LinkProps } from '..';
import cn, { Argument } from 'classnames';
import { forwardProps } from '../../utils/props';
import { Link } from '../Link/Link';

interface BreadcrumbCss {
  "fr-breadcrumb__button"?: Argument;
  "fr-breadcrumb__list"?: Argument;
  "fr-breadcrumb__link"?: Argument;
}

export interface BreadcrumbProps extends Omit<React.HTMLAttributes<HTMLDivElement>, 'className'> {
  buttonLabel?: string;
  children: React.ReactNode[] | React.ReactNode;
  className?: Argument
  css?: BreadcrumbCss;
  __TYPE?: "Breadcrumb";
}

export const Breadcrumb: React.FC<BreadcrumbProps> = ({
  buttonLabel = 'Voir le fil d’Ariane',
  children,
  className,
  css = {},
  __TYPE = "Breadcrumb",
  ...props
}) => {
  const id = useId();
  console.log("Breadcrumb", { children })
  return (
    <nav role="navigation" aria-label={props['aria-label'] || 'vous êtes ici:'} className={cn("fr-breadcrumb", className)} {...forwardProps(props as React.HTMLAttributes<HTMLDivElement>)}>
      <button className={cn("fr-breadcrumb__button", css['fr-breadcrumb__button'])} aria-expanded="false" aria-controls="breadcrumb-1">{buttonLabel || 'Voir le fil d’Ariane'}</button>
      <div className="fr-collapse" id="breadcrumb-1">
        <ol className={cn("fr-breadcrumb__list", css["fr-breadcrumb__list"])}>
          {getChildrenOfType(children, Link).filter(child => isValidElement(child)).map((child, i, { length }) => {
            return (
              <li key={`${id}-${i}`}>
                {cloneElement(child as React.ReactElement<LinkProps>, {
                  className: cn("fr-breadcrumb__link", css["fr-breadcrumb__link"]),
                  'aria-current': (i + 1 === length) ? 'page' : undefined,
                })}
              </li>
            )
          })}
        </ol>
      </div>
    </nav>
  )
}
Breadcrumb.displayName = "Breadcrumb";