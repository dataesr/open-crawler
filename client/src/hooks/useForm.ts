import { useReducer, useState } from 'react';

export default function useForm(initialState: Record<string, any>, validator: (form: Record<string, any>) => void = () => {}) {
  const [errors, setErrors] = useState(validator(initialState));
  const [form, updateForm] = useReducer((prevState: Record<string, any>, updates: Record<string, any>) => {
    const newForm = { ...prevState, ...updates };
    if (validator) {
      setErrors(validator(newForm));
    }
    return newForm;
  }, initialState);

  return { form, updateForm, errors };
}