import cn, { Argument } from "classnames";
import { forwardProps } from "../../utils/props";
import { getChildrenOfType } from "../../utils/children";
import { useId } from "react";
import { Toggle } from "./Toggle";

interface ToggleGroupProps extends Omit<React.HTMLAttributes<HTMLUListElement>, 'className'> {
  className?: Argument;
}

export const ToggleGroup: React.FC<ToggleGroupProps> = ({ children, className, ...props }) => {
  const id = useId();
  return (
    <ul className={cn('fr-toggle__list', className)} {...forwardProps(props as React.HTMLAttributes<HTMLUListElement>)}>
      {getChildrenOfType(children, Toggle).map((child, index) => <li key={`${id}-${index}`}>{child}</li>)}
    </ul>
  );
}