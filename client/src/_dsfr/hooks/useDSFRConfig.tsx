"use client";
import {
  createContext,
  useContext,
  useEffect,
  useMemo,
} from 'react';

interface ConfigContextObject {
  routerComponent?: any;
  theme?: 'system' | 'light' | 'dark';
  lang?: string;
  extendRequiredFieldsLabelsWith?: React.ReactNode;
  extendOptionalFieldsLabelsWith?: React.ReactNode;
}
export interface DSFRConfigProps extends ConfigContextObject {
  children: React.ReactNode[] | React.ReactNode;
}

const ConfigContext = createContext<ConfigContextObject>({});


export const DSFRConfig = ({
  children,
  routerComponent,
  extendRequiredFieldsLabelsWith = <span style={{ color: 'var(--text-default-error)' }}> *</span>,
  extendOptionalFieldsLabelsWith = " (optionel)",
  theme = 'system',
  lang = 'fr',
}: DSFRConfigProps) => {

  useEffect(() => {
    const currentTheme = document.documentElement.getAttribute('data-fr-scheme');
    if (!currentTheme) document.documentElement.setAttribute('data-fr-scheme', theme);
  }, [theme])

  const value: ConfigContextObject = useMemo(() => ({
    routerComponent,
    theme,
    lang,
    extendRequiredFieldsLabelsWith,
    extendOptionalFieldsLabelsWith,
  }), [routerComponent, theme, lang, extendRequiredFieldsLabelsWith, extendOptionalFieldsLabelsWith]);
  return (
    <ConfigContext.Provider value={value}>
      {children}
    </ConfigContext.Provider>
  );
};


export const useDSFRConfig = () => useContext(ConfigContext);
