// From https://blog.logrocket.com/guide-to-custom-react-hooks-with-mutationobserver/
import { useEffect, useState } from "react";

const DEFAULT_OPTIONS = {
  config: { attributes: true, childList: false, subtree: false },
};
export default function useMutationObservable(targetEl: HTMLElement | null, cb: MutationCallback, options = DEFAULT_OPTIONS) {
  const [observer, setObserver] = useState<MutationObserver | null>(null);

  useEffect(() => {
    const obs = new MutationObserver(cb);
    setObserver(obs);
  }, [cb, options, setObserver]);

  useEffect(() => {
    if (!observer) return;
    if (!targetEl) return;
    const { config } = options;
    observer.observe(targetEl, config);
    return () => {
      if (observer) {
        observer.disconnect();
      }
    };
  }, [observer, targetEl, options]);
}