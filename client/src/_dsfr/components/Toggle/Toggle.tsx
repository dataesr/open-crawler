import { forwardRef, useId } from 'react';
import cn, { Argument } from 'classnames';
import { forwardProps } from '../../utils/props';

interface ToggleCss {
  "fr-toggle__input"?: Argument;
  "fr-toggle__label"?: Argument;
  "fr-hint-text"?: Argument;
}

interface ToggleProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'className'> {
  className?: Argument;
  css?: ToggleCss;
  hasSeparator?: boolean;
  hasLabelLeft?: boolean;
  label?: string;
  id?: string;
  hint?: string;
}

export const Toggle: React.FC<ToggleProps> = forwardRef<HTMLInputElement, ToggleProps>(({
  className,
  css = {},
  hasSeparator,
  hasLabelLeft,
  label,
  id,
  hint,
  ...props
}, ref) => {
  const __id = useId();
  const _id = id || __id;
  const _className = cn('fr-toggle', {
    'fr-toggle--border-bottom': hasSeparator,
    'fr-toggle--label-left': hasLabelLeft,
  }, className);

  return (
    <div
      className={_className}
    >
      <input
        ref={ref}
        type="checkbox"
        className={cn("fr-toggle__input", css["fr-toggle__input"])}
        id={_id}
        {...forwardProps(props as React.InputHTMLAttributes<HTMLInputElement>, { exclude: ['type'] })}
      />
      <label
        className={cn("fr-toggle__label", css["fr-toggle__label"])}
        htmlFor={_id}
        data-fr-checked-label="Activé"
        data-fr-unchecked-label="Désactivé"
      >
        {label}
      </label>
      {(hint) && <p className={cn("fr-hint-text", css["fr-hint-text"])}>{hint}</p>}
    </div>
  );
});