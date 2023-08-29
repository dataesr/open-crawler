const EXCLUDED_PROPS = ['__TYPE'];

interface ForwardPropsOptions {
  exclude?: string[];
  include?: string[];
}

export function forwardProps(props: object, options: ForwardPropsOptions = {}) {
  const { include, exclude } = options
  if (include) return Object.entries(props)
    .reduce((acc, [k, v]) => include.includes(k) ? { ...acc, [k]: v } : acc, {})
  const excludedProps = exclude ? [...EXCLUDED_PROPS, ...exclude] : EXCLUDED_PROPS
  return Object.entries(props)
    .reduce((acc, [k, v]) => excludedProps.includes(k) ? acc : {...acc, [k]: v }, {})
}