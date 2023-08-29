import cn, { Argument } from "classnames";
import { forwardProps } from "../../utils/props";

interface OperatorCss {
  "fr-responsive-img": Argument;
}

export interface OperatorProps {
  className?: Argument;
  css?: OperatorCss;
  src: string;
  alt: string;
  __TYPE?: string;
}

export const Operator: React.FC<OperatorProps> = ({ src, alt, className, css = {}, ...props }) => {
  return (
    <div className={cn("fr-header__operator", className)}>
      <img className={cn("fr-responsive-img", css["fr-responsive-img"])} src={src} alt={alt} {...forwardProps(props)} />
    </div>
  )
}
Operator.defaultProps = {
  __TYPE: 'Operator'
}
Operator.displayName = 'Operator';