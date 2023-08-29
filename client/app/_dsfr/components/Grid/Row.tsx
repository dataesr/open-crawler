import cn, { Argument } from 'classnames';

interface RowProps extends Omit<React.HTMLAttributes<HTMLDivElement>, 'className'> {
  children: React.ReactNode[] | React.ReactNode;
  className?: Argument;
  gutters?: boolean;
  verticalAlign?: 'top' | 'bottom' | 'middle';
  horitontalAlign?: 'left' | 'center' | 'right';
  __TYPE?: 'Row'
}
export const Row: React.FC<RowProps> = ({
  gutters, horitontalAlign, verticalAlign, children, className,
}) => {
  const _cn = cn('fr-grid-row', {
    'fr-grid-row--gutters': gutters,
    [`fr-grid-row--${horitontalAlign}`]: horitontalAlign,
    [`fr-grid-row--${verticalAlign}`]: verticalAlign,
  }, className);
  return <div className={_cn}>{children}</div>;
};

Row.defaultProps = {
  gutters: false,
  __TYPE: 'Row',
};
Row.displayName = 'Row';
