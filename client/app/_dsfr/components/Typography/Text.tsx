import cn, { Argument } from 'classnames';
import { forwardProps } from '../../utils/props';

type TextTags = 'p' | 'span';
type TextSizes = 'xs' | 'sm' | 'md' | 'lg' | 'lead';

interface TextProps extends Omit<React.HTMLAttributes<HTMLParagraphElement | HTMLSpanElement>, 'className'> {
  children: React.ReactNode[] | React.ReactNode | string;
  className?: Argument;
  as?: TextTags;
  size?: TextSizes;
  alt?: boolean;
  bold?: boolean;
  __TYPE?: 'Text'
}

export const Text: React.FC<TextProps> = ({
  as = 'p',
  size,
  alt,
  bold,
  className,
  children,
  ...props
}) => {
  const HtmlTag = as;
  const _cn = cn(className, {
    'fr-text--alt': size !== 'lead' && alt,
    'fr-text--heavy': bold,
    [`fr-text--${size}`]: size && size !== 'md',
  });
  return (
    <HtmlTag className={_cn} {...forwardProps(props)}>
      {children}
    </HtmlTag>
  );
};

Text.defaultProps = {
  as: 'p',
  __TYPE: 'Text'
};
Text.displayName = "Text";
