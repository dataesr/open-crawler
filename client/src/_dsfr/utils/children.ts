import { Children, isValidElement } from "react";

export function getChildrenOfType(children: React.ReactNode[] | React.ReactNode, type: any) {
  const childs = Children
    .toArray(children)
    .filter((child) => (isValidElement(child)) && child.type === type)
  return childs
}
export function getChildrenOfTypes(children: React.ReactNode[] | React.ReactNode, types: any[]) {
  return Children
    .toArray(children)
    .filter((child) => (isValidElement(child)) && types.includes(child.type))
}