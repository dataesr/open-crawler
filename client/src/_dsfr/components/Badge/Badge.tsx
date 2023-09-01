import cn, { Argument } from 'classnames';
import { ColorFamily } from '../../types';
import { forwardProps } from '../../utils/props';

interface BadgeProps extends Omit<React.HTMLAttributes<HTMLParagraphElement | HTMLButtonElement>, 'className'> {
  icon?: string;
  className?: Argument;
  isSmall?: boolean;
  children: React.ReactNode;
  noIcon?: boolean;
  color?: ColorFamily;
  variant?: BadgeType;
  __TYPE?: string;
}

type BadgeType =
  | "new"
  | 'error'
  | 'info'
  | 'warning'
  | 'success';

export const Badge: React.FC<BadgeProps> = ({
  children,
  className,
  variant,
  color,
  isSmall,
  icon,
  noIcon = false,
  onClick,
  ...props
}) => {
  const _classes = cn(
    'fr-badge',
    {
      [`fr-badge--${variant}`]: variant,
      [`fr-badge--${color}`]: color,
      [`fr-icon-${icon}`]: !noIcon && icon,
      "react-dsfr-badge-icon": !noIcon && icon,
      'fr-badge--no-icon': noIcon,
      'fr-badge--sm': isSmall,
    },
    className,
  );

  if (onClick) {
    return (
      <button className={_classes} onClick={onClick} {...forwardProps(props)}>
        {children}
      </button>
    )
  }

  return (
    <p className={_classes} {...forwardProps(props)}>
      {children}
    </p>
  );
};

Badge.defaultProps = {
  __TYPE: 'Badge',
};