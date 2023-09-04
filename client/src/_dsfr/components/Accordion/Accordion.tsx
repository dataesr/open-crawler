"use client";

import cn, { Argument } from "classnames";
import { forwardRef, isValidElement, useCallback, useId, useRef, useState } from "react";
import { forwardProps } from "../../utils/props";
import useMutationObservable from "./useMutationObserver";

type AccordionCss = {
  'fr-accordion'?: Argument;
  "fr-accordion__title"?: Argument;
  "fr-accordion__btn"?: Argument;
}

export interface AccordionProps extends Omit<React.ButtonHTMLAttributes<HTMLButtonElement>, 'title' | 'className'> {
  title: React.ReactNode | string | ((expended: boolean) => React.ReactNode[] | React.ReactNode | string);
  titleAs?: React.ElementType;
  children: string | React.ReactNode[] | React.ReactNode;
  className?: Argument;
  css?: AccordionCss
  defaultExpanded?: boolean;
  __TYPE?: string;
}

export const Accordion: React.FC<AccordionProps> = forwardRef<HTMLButtonElement, AccordionProps>(({
  title,
  titleAs = 'h3',
  children,
  className,
  css = {},
  defaultExpanded = false,
  ...props
}, ref) => {
  const id = useId();
  const buttonRef = useRef(null);
  const [expanded, setExpanded] = useState<boolean>(!!defaultExpanded);
  const TitleElement = titleAs;

  const onButtonMutation = useCallback(
    (mutationList: MutationRecord[]) => {
      const mutation: MutationRecord | undefined = mutationList.find((record: MutationRecord) => record.attributeName === 'aria-expanded');
      if (mutation) {
        setExpanded(buttonRef?.current?.['attributes']?.['aria-expanded']?.['value'] === "true" ? true : false);
      }
    },
    []
  );

  useMutationObservable(buttonRef?.current, onButtonMutation);

  return (
    <section
      ref={ref}
      className={cn("fr-accordion", css['fr-accordion'])}
    >
      <TitleElement
        className={cn("fr-accordion__title", css["fr-accordion__title"])}
      >
        <button
          {...forwardProps(props as React.ButtonHTMLAttributes<HTMLButtonElement>)}
          ref={buttonRef}
          className={cn("fr-accordion__btn", css["fr-accordion__btn"])}
          aria-expanded={defaultExpanded}
          aria-controls={id}
        >
          {(isValidElement(title) || typeof title === 'string')
            ? title
            : (typeof title === 'function')
              ? title(expanded)
              : null}
        </button>
      </TitleElement>
      <div className="fr-collapse" id={id}>
        {children}
      </div>
    </section>
  )
});

Accordion.defaultProps = {
  titleAs: 'h3',
  __TYPE: 'Accordion'
};
Accordion.displayName = 'Accordion';