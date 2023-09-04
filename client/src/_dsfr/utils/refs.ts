export type RefArray = (React.ForwardedRef<HTMLElement> | React.RefObject<HTMLElement> | React.MutableRefObject<HTMLElement> | React.RefCallback<HTMLElement> | null | undefined)[]

export default function mergeRefs(node: HTMLElement | null | undefined, refs: RefArray) {
  if (!node) return;
  refs.forEach((ref) => {
    if (typeof ref === 'function') {
      ref(node);
    } else if (ref) {
      (ref as React.MutableRefObject<HTMLElement>).current = node
    }
  })
}