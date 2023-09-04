import { forwardRef } from 'react';
import cn, { Argument } from 'classnames';
import { forwardProps } from '../../utils/props';

export interface ContainerProps extends Omit<React.HTMLAttributes<HTMLDivElement>, 'className'> {
  as?: 'article' | 'aside' | 'header' | 'footer' | 'main' | 'nav' | 'section' | 'div';
  fluid?: boolean;
  fluidFrom?: 'xs' | 'sm' | 'md' | 'lg' | 'xl';
  className?: Argument;
  children?: React.ReactNode[] | React.ReactNode | string;
  __TYPE?: 'Container';
}

export const Container = forwardRef<HTMLDivElement, ContainerProps>(({
  as = "div",
  children,
  className,
  fluid = false,
  fluidFrom = "xs",
  ...props
}, ref) => {
  const HtmlTag = as;
  return (
    <HtmlTag
      className={cn({
        'fr-container': !fluid,
        'fr-container-fluid': (fluid || !(fluidFrom !== 'xs')),
        [`fr-container-${fluidFrom}--fluid`]: (!fluid && fluidFrom !== 'xs')
      }, className)}
      ref={ref}
      {...forwardProps(props as React.HTMLAttributes<HTMLDivElement>)}
    >
      {children}
    </HtmlTag>
  );
});

Container.defaultProps = {
  __TYPE: 'Container',
};
Container.displayName = "Container";