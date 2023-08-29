import cn, { Argument } from 'classnames';
import { forwardProps } from '../../utils/props';

type TitleTags = 'h1' | 'h2' | 'h3' | 'h4' | 'h5' | 'h6';
type TitleDisplay = 'xs' | 'sm' | 'md' | 'lg' | 'xl';
type Look = TitleTags & TitleDisplay;

interface TitleProps extends Omit<React.HTMLAttributes<HTMLHeadingElement>, 'className'> {
  as?: TitleTags;
  children: React.ReactNode[] | React.ReactNode | string;
  className?: Argument;
  look?: 'h1' | 'h2' | 'h3' | 'h4' | 'h5' | 'h6';
  __TYPE?: 'Title'
}

export const Title: React.FC<TitleProps> = ({
  as = 'h1',
  children,
  className,
  look,
  __TYPE = 'Title',
  ...props
}) => {
  const display = look && ['xs', 'sm', 'md', 'lg', 'xl'].includes(look);
  const HtmlTag = as;

  const _cn = cn(className, {
    [`fr-${look}`]: (!display && look && look !== as),
    [`fr-display-${look}`]: display,
  });
  return (
    <HtmlTag className={_cn} {...forwardProps(props)}>
      {children}
    </HtmlTag>
  );
};

Title.displayName = "Title";