import { useState, useRef, forwardRef, useId } from 'react';
import cn, { Argument } from 'classnames';
import { forwardProps } from '../../utils/props';
import mergeRefs from '../../utils/refs';
import { useDSFRConfig } from '../../hooks/useDSFRConfig';

interface InputCss {
  'fr-label'?: Argument;
  'fr-hint-text'?: Argument;
  'fr-input'?: Argument;
  'fr-input-wrap'?: Argument;
}

export type InputProps = {
  className?: Argument;
  css?: InputCss;
  disableAutoValidation?: boolean;
  textarea?: boolean;
  message?: string;
  messageType?: 'error' | 'valid' | '' | null;
  label?: string;
  hint?: string | React.ReactNode;
  icon?: string;
  onBlur?: (event: React.FocusEvent<HTMLInputElement | HTMLTextAreaElement>) => void;
  onChange?: (event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => void;
} & (React.InputHTMLAttributes<HTMLInputElement> | React.TextareaHTMLAttributes<HTMLTextAreaElement>);

export const Input: React.FC<InputProps> = forwardRef<HTMLInputElement | HTMLTextAreaElement, InputProps>(({
  className,
  css = {},
  disableAutoValidation = false,
  textarea,
  hint,
  icon,
  id,
  label,
  message,
  messageType,
  onBlur,
  onChange,
  ...props
}, ref) => {
  const _id = useId();
  const { extendRequiredFieldsLabelsWith, extendOptionalFieldsLabelsWith } = useDSFRConfig();
  const [inputState, setInputState] = useState('');
  const inputId = id || _id;
  const inputRef = useRef<HTMLInputElement | HTMLTextAreaElement>(null);
  const isInputStateControlled = message !== undefined || messageType !== undefined;

  const inputClass = cn('fr-input', {
    'fr-input--error': isInputStateControlled ? messageType === 'error' : inputState === 'error',
    'fr-input--valid': isInputStateControlled ? messageType === 'valid' : inputState === 'valid',
  }, css['fr-input']);
  const inputGroupClass = cn('fr-input-group', {
    'fr-input-group--error': isInputStateControlled ? messageType === 'error' : inputState === 'error',
    'fr-input-group--valid': isInputStateControlled ? messageType === 'valid' : inputState === 'valid',
    'fr-input-group--disabled': props.disabled,
  }, className);

  const handleBlur = (e: React.FocusEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const inputElement = inputRef.current;
    if (!disableAutoValidation && !isInputStateControlled && inputElement) {
      setInputState(inputElement.checkValidity() ? 'valid' : 'error');
    }
    if (onBlur) onBlur(e);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const inputElement = inputRef.current;
    if (!disableAutoValidation && !isInputStateControlled && inputElement && inputState) {
      setInputState(inputElement.checkValidity() ? 'valid' : 'error');
    }
    if (onChange) onChange(e);
  };

  const stateMessage = (isInputStateControlled || disableAutoValidation)
    ? (messageType && (<p className={`fr-${messageType || 'error'}-text`} id={`${inputId}-message`}>{message}</p>))
    : ((inputState === 'error' && !disableAutoValidation) && (<p className={`fr-${inputState || 'error'}-text`} id={`${inputId}-message`}>{inputRef.current?.validationMessage}</p>))


  return (
    <div className={inputGroupClass}>
      <label className={cn("fr-label", css['fr-label'])} htmlFor={inputId}>
        {label}
        {props.required ? extendRequiredFieldsLabelsWith : extendOptionalFieldsLabelsWith}
        {hint && <span className={cn("fr-hint-text", css['fr-hint-text'])}>{hint}</span>}
      </label>
      <div className={cn('fr-input-wrap', { [`fr-icon-${icon}`]: icon }, css['fr-input-wrap'])}>
        {textarea ? (
          <textarea
            id={inputId}
            className={inputClass}
            onBlur={handleBlur}
            onChange={handleChange}
            ref={(node) => mergeRefs(node, [ref, inputRef])}
            aria-describedby={stateMessage ? `${inputId}-message` : undefined}
            {...(forwardProps(props) as React.TextareaHTMLAttributes<HTMLTextAreaElement>)}
          />
        ) : (
          <input
            id={inputId}
            className={inputClass}
            onBlur={handleBlur}
            onChange={handleChange}
            ref={(node) => mergeRefs(node, [ref, inputRef])}
            aria-describedby={stateMessage ? `${inputId}-message` : undefined}
            {...(forwardProps(props) as React.InputHTMLAttributes<HTMLInputElement>)}
          />
        )}
      </div>
      {stateMessage && stateMessage}
    </div>
  );
});
