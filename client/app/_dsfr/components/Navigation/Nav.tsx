import { cloneElement, isValidElement, useId } from 'react';
import { getChildrenOfTypes } from '../../utils/children';
import { forwardProps } from '../../utils/props';
import cn, { Argument } from 'classnames';
import { LinkProps, Link } from '../Link';
import { NavItem } from './NavItem';

interface NavCss {
  'fr-nav__list'?: Argument;
  "fr-nav__item"?: Argument;
}

export interface NavProps extends Omit<React.HTMLAttributes<HTMLDivElement>, 'className'> {
  children: React.ReactNode[] | React.ReactNode;
  className?: Argument;
  css?: NavCss;
  id?: string;
  __TYPE?: string;
}

export const Nav: React.FC<NavProps> = ({
  children,
  className,
  css = {},
  id,
  ...props
}) => {
  const localId = useId();
  const _id = id || localId;
  return (
    <nav className={cn("fr-nav", className)} id={_id} role="navigation" {...forwardProps(props as React.HTMLAttributes<HTMLDivElement>)}>
      <ul className={cn('fr-nav__list', css['fr-nav__list'])}>
        {getChildrenOfTypes(children, [NavItem, Link]).map((child, i) => (
          isValidElement(child) && (
            <li className={cn("fr-nav__item", css["fr-nav__item"])} key={`navitem-${_id}-${i}`}>
              {
                (child.type === Link)
                  ? cloneElement((child as React.ReactElement<LinkProps>), { className: cn("fr-nav__link", child.props.className) })
                  : child
              }
            </li>
          )
        ))}
      </ul>
    </nav>
  );
};

Nav.defaultProps = {
  __TYPE: 'Nav',
};