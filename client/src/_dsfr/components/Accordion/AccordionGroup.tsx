"use client";
import { Fragment, useId } from "react";
import { getChildrenOfType } from "../../utils/children";
import cn, { Argument } from "classnames";

export interface AccordionGroupProps {
  children: React.ReactNode[] | React.ReactNode;
  className?: Argument;
  __TYPE?: string;
}

export const AccordionGroup: React.FC<AccordionGroupProps> = ({ children, className }) => {
  const id = useId()
  return (
    <div className={cn("fr-accordions-group", className)}>
      {getChildrenOfType(children, 'Accordion').map((child, index) => <Fragment key={`${id}-d${index}`}>{child}</Fragment>)}
    </div>
  )
}
AccordionGroup.defaultProps = {
  __TYPE: 'AccordionGroup'
};
AccordionGroup.displayName = 'AccordionGroup';