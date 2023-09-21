import cn, { Argument } from "classnames";
import { useEffect, useRef } from "react";
import { ColorType } from "../../types";
import { forwardProps } from "../../utils/props";

interface NoticeCss {
  "fr-container"?: Argument;
  "fr-notice__body"?: Argument;
  "fr-notice__title"?: Argument;
  "fr-btn--close"?: Argument;
}

export interface NoticeProps extends Omit<React.HTMLAttributes<HTMLDivElement>, 'className'> {
  closeMode?: "disallow" | "uncontrolled" | "controlled" | "autoDismiss";
  autoDismissAfter?: number;
  onClose?: (e: React.MouseEvent<HTMLButtonElement>) => void;
  children?: string | React.ReactNode[] | React.ReactNode;
  className?: Argument;
  css?: NoticeCss;
  type: ColorType;
}

export const Notice: React.FC<NoticeProps> = ({
  children,
  closeMode = "disallow",
  autoDismissAfter = 5000,
  type = 'info',
  className,
  css = {},
  onClose,
  ...props
}) => {
  const ref = useRef<HTMLDivElement>(null);

  const handleClose = (e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();
    ref.current?.remove();
    if (onClose) onClose(e);
  }

  useEffect(() => {
    if (closeMode === "autoDismiss") {
      const timeout = setTimeout(() => {
        ref.current?.remove();
      }, autoDismissAfter);
      return () => clearTimeout(timeout);
    }
  }, [closeMode, autoDismissAfter, onClose])
  const _cn = cn('fr-notice', {
    "fr-notice--info": type === 'info',
    [`react-dsfr-notice--${type}`]: type !== 'info',
  }, className)
  return (
    <div ref={ref} className={_cn} {...forwardProps(props as React.HTMLAttributes<HTMLDivElement>)}>
      <div className={cn("fr-container", css["fr-container"])}>
        <div className={cn("fr-notice__body", css["fr-notice__body"])}>
          <p className={cn("fr-notice__title", css["fr-notice__title"])}>{children}</p>
          {(closeMode !== "disallow") && (<button
            onClick={(closeMode === "uncontrolled") ? handleClose : onClose}
            className={cn("fr-btn--close", "fr-btn", css["fr-btn--close"])}
          >
            Masquer le message
          </button>)}
        </div>
      </div>
    </div>
  )
}