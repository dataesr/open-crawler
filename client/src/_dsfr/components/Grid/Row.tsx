import cn, { Argument } from 'classnames';

interface RowProps extends Omit<React.HTMLAttributes<HTMLDivElement>, 'className'> {
  children: React.ReactNode[] | React.ReactNode;
  className?: Argument;
  gutters?: boolean;
  verticalAlign?: 'top' | 'bottom' | 'middle';
  horizontalAlign?: 'left' | 'center' | 'right';
  __TYPE?: 'Row'
}
export const Row: React.FC<RowProps> = ({
  gutters, horizontalAlign, verticalAlign, children, className,
}) => {
  const _cn = cn('fr-grid-row', {
    'fr-grid-row--gutters': gutters,
    [`fr-grid-row--${horizontalAlign}`]: horizontalAlign,
    [`fr-grid-row--${verticalAlign}`]: verticalAlign,
  }, className);
  return <div className={_cn}>{children}</div>;
};

Row.defaultProps = {
  gutters: false,
  __TYPE: 'Row',
};
Row.displayName = 'Row';
