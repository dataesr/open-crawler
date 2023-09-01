import { useId, isValidElement, cloneElement } from 'react';
import { getChildrenOfTypes } from '../../utils/children';
import { forwardProps } from '../../utils/props';
import cn, { Argument } from 'classnames';
import { LinkProps } from '../Link';

interface NavItemCss {
  "fr-menu"?: Argument;
  "fr-menu__list"?: Argument;
}

type NavItemProps = {
  children?: React.ReactNode[] | React.ReactNode;
  className?: Argument;
  css?: NavItemCss;
  current?: boolean;
  href?: string;
  title: string;
  __TYPE?: 'NavItem';
} & (React.HTMLAttributes<HTMLAnchorElement> | React.HTMLAttributes<HTMLButtonElement>)

export const NavItem: React.FC<NavItemProps> = ({
  children,
  className,
  current = false,
  css = {},
  href,
  title,
  ...props
}) => {
  const id = useId()
  const childs = getChildrenOfTypes(children, ['NavItem', 'Link']);
  return (
    <>
      <button
        className={cn("fr-nav__btn", className)}
        aria-expanded="false"
        aria-controls={id}
        aria-current={current || undefined}
        {...forwardProps(props as React.HTMLAttributes<HTMLButtonElement>)}
      >
        {title}
      </button>
      <div className={cn("fr-collapse", "fr-menu", css["fr-menu"])} id={id}>
        <ul className={cn("fr-menu__list", css["fr-menu__list"])}>
          {childs.map((child, i) => (
            <li className="fr-nav__item" key={`navitem-${id}-${i}`}>
              {
                (isValidElement(child) && child.props.__TYPE === 'Link')
                  ? cloneElement((child as React.ReactElement<LinkProps>), { className: cn("fr-nav__link", child.props.className) })
                  : child
              }
            </li>
          ))}
        </ul>
      </div>
    </>
  )
};

NavItem.defaultProps = {
  __TYPE: 'NavItem',
};