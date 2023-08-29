"use client";
import { forwardRef } from 'react';
import { useDSFRConfig } from '../../hooks/useDSFRConfig';
import { forwardProps } from '../../utils/props';
import cn, { Argument } from 'classnames';

export interface LinkProps extends Omit<React.AnchorHTMLAttributes<HTMLAnchorElement>, 'className'> {
  className?: Argument;
  size?: "sm" | "md" | "lg";
  icon?: string;
  iconPosition?: "left" | "right";
  isSimple?: boolean;
  current?: boolean;
  external?: boolean;
  __TYPE?: string;
}

export const Link: React.FC<LinkProps> = forwardRef<HTMLAnchorElement, LinkProps>(({
  children,
  className,
  icon,
  current,
  iconPosition = "left",
  external = false,
  isSimple = false,
  size = "md",
  __TYPE = "Link",
  ...props
}, ref,
) => {
  const { routerComponent: RouterComponent } = useDSFRConfig();
  const Component = external ? 'a' : RouterComponent || 'a';
  return (
    <Component
      ref={ref}
      aria-current={current || undefined}
      className={cn({
        'fr-link': isSimple,
        [`fr-link-${size}`]: size !== 'md',
        [`fr-icon-${icon}`]: isSimple && !!icon,
        [`fr-link--icon-${iconPosition}`]: (isSimple && icon),
      }, className)}
      {...forwardProps(props as React.AnchorHTMLAttributes<HTMLAnchorElement>)}
    >
      {children}
    </Component>
  );
})

Link.displayName = "Link";
