"use client";

import { forwardRef, useId, useRef } from 'react';
import cn, { Argument } from 'classnames';
import { forwardProps } from '../../utils/props';
import mergeRefs from '../../utils/refs';

interface SearchBarCss {
  "fr-label"?: Argument;
  "fr-btn"?: Argument;
  "fr-input"?: Argument;
}
export type SearchBarProps = {
  buttonLabel?: string;
  className?: Argument;
  css?: SearchBarCss;
  placeholder?: string;
  label?: string;
  onSearch: (text?: string) => void;
  isLarge?: boolean;
  id?: string;
} & (React.InputHTMLAttributes<HTMLInputElement>)

export const SearchBar: React.FC<SearchBarProps> = forwardRef<HTMLInputElement, SearchBarProps>(({
  className,
  css = {},
  buttonLabel,
  id,
  isLarge,
  label,
  onSearch,
  ...props
}, ref) => {
  const localId = useId();
  const _ref = useRef<HTMLInputElement | null>(null);
  const _id = id || localId;
  const onKeyDown = (e: React.KeyboardEvent) => (e.key === 'Enter') && onSearch(_ref.current?.value);
  return (
    <div
      role="search"
      className={cn('fr-search-bar', { 'fr-search-bar--lg': isLarge }, className)}
    >
      {label && <label className={cn("fr-label", css["fr-label"])} htmlFor={_id}>{label}</label>}
      <input
        ref={(node) => mergeRefs(node, [ref, _ref])}
        className={cn("fr-input", css["fr-input"])}
        type="search"
        id={_id}
        onKeyDown={onKeyDown}
        {...forwardProps(props as React.HTMLAttributes<HTMLInputElement>)}
      />
      <button
        type="button"
        onClick={() => onSearch(_ref.current?.value)}
        className={cn('fr-btn', { 'fr-btn--lg': isLarge }, css['fr-btn'])}
        title={buttonLabel}
      >
        {buttonLabel}
      </button>
    </div>
  );
});

SearchBar.displayName = 'SearchBar';


