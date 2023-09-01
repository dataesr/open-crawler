import { Fragment } from "react";

export interface LogoProps {
  text: string;
  __TYPE?: string;
}

export const Logo: React.FC<LogoProps> = ({ text }) => {
  const lines = text.split('|');
  const brText = lines.reduce<JSX.Element[]>((acc, cur, i) => {
    return (i > 0)
      ? [...acc, <br key={`br-${i}`} />, <Fragment key={i}>{cur}</Fragment>]
      : [<Fragment key={i}>{cur}</Fragment>]
  }, []);
  return (
    <div className="fr-header__logo">
      <p className="fr-logo">
        {brText}
      </p>
    </div>
  )
}
Logo.defaultProps = {
  __TYPE: 'Logo',
}
Logo.displayName = 'Logo';