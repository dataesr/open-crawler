import cn, { Argument } from 'classnames';
import { useId } from "react";
import { getChildrenOfType } from "../../utils/children";
import { forwardProps } from '../../utils/props';
import { Button } from '../Button';

export interface FastAccessCss {
  "fr-btns-group": Argument;
}

export interface FastAccessProps extends Omit<React.HTMLAttributes<HTMLDivElement>, 'className'> {
  children: React.ReactNode[] | React.ReactNode;
  className?: Argument;
  css?: FastAccessCss
  __TYPE?: string;
}

export const FastAccess: React.FC<FastAccessProps> = ({ children, className, css = {}, ...props }) => {
  const id = useId()
  return (
    <div className={cn("fr-header__tools-links", className)} {...forwardProps(props)}>
      <ul className={cn("fr-btns-group", css["fr-btns-group"])}>
        {getChildrenOfType(children, Button).map((child: React.ReactNode, i) => (<li key={`${id}-${i}`}>{child}</li>))}
      </ul>
    </div>
  )
}
FastAccess.defaultProps = {
  __TYPE: 'FastAccess'
}
FastAccess.displayName = 'FastAccess';