import { useEffect, useState } from 'react';
import { Col, Row, Input, BadgeGroup, Badge } from '../_dsfr'

type TagInputProps = {
  label: string;
  hint?: string;
  tags: string[];
  onTagsChange: (tags: string[]) => void;
}

export default function TagInput({ label, hint, tags, onTagsChange }: TagInputProps) {
  const [input, setInput] = useState('');
  const [values, setValues] = useState(tags);

  const handleKeyDown = (e: any) => {
    if ([13, 9].includes(e.keyCode) && input) {
      e.preventDefault();
      if (values.includes(input.trim())) return;
      const newValues = [...values, input.trim()];
      setValues(newValues);
      setInput('');
      onTagsChange(newValues);
    }
  };

  const handleDeleteClick = (tag: string) => {
    const newValues = [...values.filter((el: string) => el !== tag)];
    setValues(newValues);
    onTagsChange(newValues);
  };

  useEffect(() => setValues(tags), [tags]);

  return (
    <>
      <Row verticalAlign="bottom">
        <Col>
          <Input
            css={{ 'fr-input': "input40" }}
            type="text"
            value={input}
            label={label}
            hint={hint}
            onChange={(e: any) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
          />
        </Col>
      </Row>
      <Row>
        <Col className="fr-pt-2w">
          <BadgeGroup>
            {values.map((tag: string) => (
              <Badge
                key={tag}
                color="yellow-tournesol"
                className="fr-mr-1w"
                icon="close-line"
                onClick={() => handleDeleteClick(tag)}
              >
                {tag}
              </Badge>
            ))}
          </BadgeGroup>
        </Col>
      </Row>
    </>
  );
}

TagInput.defaultProps = {
  hint: 'Valider votre ajout avec la touche "Entrée"',
  tags: [],
};