import { Link } from "../Link";
import { forwardProps } from "../../utils/props";
import cn, { Argument } from "classnames";

interface ServiceCss {
  "fr-header__service-title"?: Argument;
  "fr-header__service-tagline"?: Argument;
}

export interface ServiceProps {
  className?: Argument;
  css?: ServiceCss;
  href?: string;
  name: string;
  tagline?: string;
  __TYPE?: string;
}

export const Service: React.FC<ServiceProps> = ({ href, name, tagline, className, css = {}, ...props }) => {
  return (
    <div className={cn("fr-header__service", className)}>
      <p className={cn("fr-header__service-title", css["fr-header__service-title"])}>
        <Link href={href} {...forwardProps(props)}>
          {name}
        </Link>
      </p>
      {tagline && <p className={cn("fr-header__service-tagline", css["fr-header__service-tagline"])}>{tagline}</p>}
    </div>
  )
}
Service.defaultProps = {
  href: '/',
  __TYPE: 'Service',
}
Service.displayName = 'Service';