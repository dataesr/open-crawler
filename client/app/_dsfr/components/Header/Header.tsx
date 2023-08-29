
import cn, { Argument } from 'classnames';
import { useId, isValidElement } from "react";
import { getChildrenOfType } from "../../utils/children";
import { forwardProps } from '../../utils/props';
import { FastAccess } from './FastAccess';
import { SearchBar } from '../SearchBar';
import { Nav } from '../Navigation';
import { Logo } from '../Logo';
import { Operator } from './Operator';
import { Service } from './Service';


interface HeaderCss {
  "fr-header__body"?: Argument;
  "fr-header__body-row"?: Argument;
  "fr-header__brand"?: Argument;
  "fr-header__brand-top"?: Argument;
  "fr-header__navbar"?: Argument;
  "fr-btn--search"?: Argument;
  "fr-btn--menu"?: Argument;
  "fr-header__tools"?: Argument;
  "fr-header__search"?: Argument;
  "fr-header__menu"?: Argument;
  "fr-header__menu-links"?: Argument;
}

export interface HeaderProps extends Omit<React.HTMLAttributes<HTMLDivElement>, 'className'> {
  children: React.ReactNode[] | React.ReactNode;
  className?: Argument;
  css?: HeaderCss;
}

export const Header: React.FC<HeaderProps> = ({ children, className, css = {}, ...props }) => {
  const searchId = useId();
  const searchModalId = useId();
  const menuModalId = useId();
  const menuId = useId();
  const service = getChildrenOfType(children, Service)?.[0];
  const fastAccess = getChildrenOfType(children, FastAccess)?.[0];
  const searchBar = getChildrenOfType(children, SearchBar)?.[0];
  const menu = getChildrenOfType(children, Nav)?.[0];
  const logo = getChildrenOfType(children, Logo);
  const operator = getChildrenOfType(children, Operator);
  const searchTitle = isValidElement(searchBar) ? searchBar.props.title : 'Rechercher';
  return (
    <header role="banner" className={cn("fr-header", className)} {...forwardProps(props)}>
      <div className={cn("fr-header__body", css["fr-header__body"])}>
        <div className="fr-container">
          <div className={cn("fr-header__body-row", css["fr-header__body-row"])}>
            <div className={cn("fr-header__brand fr-enlarge-link", css["fr-header__brand"])}>
              <div className={cn("fr-header__brand-top", css["fr-header__brand-top"])}>
                {logo && logo}
                {operator && operator}
                {(fastAccess || searchBar) && (
                  <div className={cn("fr-header__navbar", css["fr-header__navbar"])}>
                    {(searchBar) && (
                      <button className={cn("fr-btn--search fr-btn", css["fr-btn--search"])} data-fr-opened="false" aria-controls={searchModalId} id={searchId} title={searchTitle}>
                        {searchTitle}
                      </button>
                    )}
                    {(fastAccess) && (
                      <button className={cn("fr-btn--menu fr-btn", css["fr-btn--menu"])} data-fr-opened="false" aria-controls={menuModalId} aria-haspopup="menu" id={menuId} title="Menu">
                        Menu
                      </button>
                    )}
                  </div>
                )}
              </div>
              {service && service}
            </div>
            <div className={cn("fr-header__tools", css["fr-header__tools"])}>
              {fastAccess}
              {searchBar && (
                <div className={cn("fr-header__search fr-modal", css["fr-header__search"])} id={searchModalId}>
                  <div className="fr-container fr-container-lg--fluid">
                    <button className="fr-btn--close fr-btn" aria-controls={searchModalId} title="Fermer">
                      Fermer
                    </button>
                    {searchBar}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
      <div className={cn("fr-header__menu fr-modal", css["fr-header__menu"])} id={menuModalId} aria-labelledby={menuId}>
        <div className="fr-container">
          <button className="fr-btn--close fr-btn" aria-controls={menuModalId} title="Fermer">
            Fermer
          </button>
          <div className={cn("fr-header__menu-links", css["fr-header__menu-links"])} />
          {menu && menu}
        </div>
      </div>
    </header>
  )
}
Header.displayName = 'Header';