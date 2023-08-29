import { forwardRef } from 'react';
import cn, { Argument } from 'classnames';
import { ColorFamily, ColorType } from '../../types';
import { Link, LinkProps } from '../Link';
import { forwardProps } from '../../utils/props';

type DefaultColor = 'blue-france'

type ButtonProps = {
  children?: string;
  className?: Argument
  color?: ColorFamily | ColorType | DefaultColor;
  href?: string;
  icon?: string;
  iconPosition?: 'left' | 'right';
  size?: 'sm' | 'md' | 'lg';
  type?: 'submit' | 'reset' | 'button';
  variant?: 'primary' | 'secondary' | 'tertiary' | 'text';
  __TYPE?: string;
} & (React.ButtonHTMLAttributes<HTMLButtonElement> | React.AnchorHTMLAttributes<LinkProps>)

export const Button: React.FC<ButtonProps> = forwardRef<any, ButtonProps>(({
  children,
  className,
  color,
  icon,
  iconPosition = 'left',
  type = 'button',
  size = 'md',
  variant = 'primary',
  ...props
}, ref) => {
  const _classes = cn(
    'fr-btn',
    {
      [`fr-btn--${size}`]: size !== 'md',
      [`react-dsfr-btn--${color}`]: (!!color && color !== 'blue-france'),
      'fr-btn--secondary': variant === 'secondary',
      'fr-btn--tertiary': variant === 'tertiary',
      'fr-btn--tertiary-no-outline': variant === 'text',
      [`fr-icon-${icon}`]: !!icon,
      [`fr-btn--icon-${iconPosition}`]: (icon && children),
      'fr-btn--icon': (icon && !children),
    },
    className,
  );
  const HTMLTag: typeof Link | 'button' = (props.href) ? Link : 'button';
  return (
    <HTMLTag className={_classes} ref={ref} {...forwardProps(props)}>
      {children || ''}
    </HTMLTag>
  );
})

Button.defaultProps = {
  __TYPE: "Button",
}
Button.displayName = "Button";
