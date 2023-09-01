import classNames from 'classnames';
import { getChildrenOfType } from '../../utils/children';
import { forwardProps } from '../../utils/props';
import { useId } from 'react';
import { Badge } from './Badge';

export interface BadgeGroupProps {
  className?: string;
  children: React.ReactNode[] | React.ReactNode;
  __TYPE?: string;
}
export const BadgeGroup: React.FC<BadgeGroupProps> = ({
  children,
  className,
  ...props
}) => {
  const id = useId();
  const _classes = classNames('fr-badges-group', className);
  return (
    <ul className={_classes} {...forwardProps(props)}>
      {getChildrenOfType(children, Badge).map((child, index) => <li key={`${id}-${index}`}>{child}</li>)}
    </ul>
  );
};

BadgeGroup.displayName = 'BadgeGroup';