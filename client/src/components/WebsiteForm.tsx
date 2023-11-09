import React, { ChangeEvent } from 'react';
import { Button, Col, Container, Input, Row, Text, Toggle, ToggleGroup } from '../_dsfr';
import useForm from '../hooks/useForm';
import { WebsiteFormBody } from '../_types/websites';
import TagInput from './TagInput';

const DEFAULT_INITIAL_FORM = {
  url: '',
  crawl_every: 30,
  depth: 2,
  limit: 400,
  tags: [],
  headers: {},
  lighthouse: { enabled: true, depth: 0 },
  carbon_footprint: { enabled: true, depth: 0 },
  responsiveness: { enabled: true, depth: 0 },
  technologies_and_trackers: { enabled: true, depth: 0 },
} as WebsiteFormBody;

type WebsiteFormProps = {
  onSubmit: (form: WebsiteFormBody) => void,
  initialForm?: WebsiteFormBody,
  create?: boolean,
  isLoading?: boolean,
  notice?: null | React.ReactNode
}

function sanitize(form: Record<string, any>): WebsiteFormBody {
  const fields = [
    'url', 'crawl_every', 'depth', 'limit', 'tags', 'headers',
    'lighthouse', 'carbon_footprint', 'responsiveness',
    'technologies_and_trackers'
  ];
  const body: Record<string, any> = {};
  Object.keys(form).forEach((key) => { if (fields.includes(key)) { body[key] = form[key]; } });
  return body as WebsiteFormBody;
}

export default function WebsiteForm({
  onSubmit,
  initialForm = DEFAULT_INITIAL_FORM,
  create = true,
  isLoading = false,
  notice = null,
}: WebsiteFormProps) {
  const { form, updateForm, touched } = useForm(initialForm);

  return (
    <Container fluid>
      <form noValidate onSubmit={(e) => {
        e.preventDefault();
        const body = sanitize(form);
        console.log('SUBMIT', body);
        onSubmit(body)
      }}>
        <Row className="fr-mb-5w">
          <Col>
            <Input
              css={{ 'fr-input': "input40" }}
              required
              disabled={!create}
              hint="Saississez l'URL du site web à crawler, en précisant le protocole (http:// ou https://)"
              type="url"
              label="URL du site web"
              value={form.url}
              onChange={(e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => updateForm({ url: e.target.value })}
            />
          </Col>
        </Row>
        <hr />
        <Row className="fr-mb-5w">
          <Col>
            <TagInput
              label="Ajouter des tags au site web"
              tags={form.tags}
              onTagsChange={(tags) => updateForm({ tags: tags.map((tag) => tag.toUpperCase()) })}
            />
          </Col>
        </Row>
        <hr />
        <Text size="lead" bold>Récurrence</Text>
        <Row className="fr-mb-5w">
          <Col>
            <Input
              css={{ 'fr-input': "input10" }}
              required
              label="Récurrence du crawl en jours"
              min="1"
              max="365"
              defaultValue="30"
              type="number"
              hint="Par exemple, si vous souhaitez recrawler tous les trente jours entrez '30'"
              value={form.crawl_every}
              onChange={(e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => updateForm({ crawl_every: parseInt(e.target.value, 10) })}
            />
          </Col>
        </Row>
        <hr />
        <Text size="lead" bold>Paramètres de crawl</Text>
        <Row className="fr-mb-5w">
          <Col>
            <Input
              css={{ 'fr-input': "input10" }}
              required
              min="0"
              max="5"
              defaultValue="2"
              label="Profondeur maximal du crawl"
              hint={<>
                Par exemple, si vous souhaitez crawler jusqu'à 2 niveaux de profondeur, entrez 2.
                <br />
                0 correspond à un crawl de la page d'acceuil uniquement.
              </>}
              type="number"
              value={form.depth}
              onChange={(e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => updateForm({ depth: parseInt(e.target.value, 10) })}
            />
          </Col>
        </Row>
        <Row className="fr-mb-5w">
          <Col>
            <Input
              css={{ 'fr-input': "input10" }}
              required
              min="1"
              max="1000"
              defaultValue="400"
              label="Nombre de page maximum à crawler"
              hint="Par exemple, si vous souhaitez crawler 400 pages maximum, entrez '400'"
              type="number"
              value={form.limit}
              onChange={(e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => updateForm({ limit: parseInt(e.target.value, 10) })}
            />
          </Col>
        </Row>
        <hr />
        <Text size="lead" bold>Metadata</Text>
        <Row className="fr-mb-5w">
          <Col xs="12" sm="8" md="6">
            <ToggleGroup>
              <Toggle
                defaultChecked={form.lighthouse.enabled}
                hasLabelLeft
                label="Lighthouse"
                hint="Désactivez cette option si vous ne souhaitez pas crawler les informations de lighthouse."
                onChange={(e: ChangeEvent<HTMLInputElement>) => updateForm({ lighthouse: { enabled: e.target.checked, depth: 0 } })}
              />
              <Toggle
                defaultChecked={form.technologies_and_trackers.enabled}
                hasLabelLeft
                label="Technology et tracker"
                hint="Désactivez cette option si vous ne souhaitez pas crawler les informations de technologies et de trackers."
                onChange={(e: ChangeEvent<HTMLInputElement>) => updateForm({ technologies_and_trackers: { enabled: e.target.checked, depth: 0 } })}
              />
              <Toggle
                defaultChecked={form.responsiveness.enabled}
                hasLabelLeft
                label="Responsive"
                hint="Désactivez cette option si vous ne souhaitez pas crawler les informations de responsive."
                onChange={(e: ChangeEvent<HTMLInputElement>) => updateForm({ responsiveness: { enabled: e.target.checked, depth: 0 } })}
              />
              <Toggle
                defaultChecked={form.carbon_footprint.enabled}
                hasLabelLeft
                label="Empreinte carbon"
                hint="Désactivez cette option si vous ne souhaitez pas crawler les informations d'empreinte carbon."
                onChange={(e: ChangeEvent<HTMLInputElement>) => updateForm({ carbon_footprint: { enabled: e.target.checked, depth: 0 } })}
              />
            </ToggleGroup>
          </Col>
        </Row>
        <hr />
        <div style={{ display: 'flex' }}>
          <div>

            <Button disabled={isLoading || !touched} className={notice ? "fr-mr-2w" : ""} size="lg" type="submit">
              {create ? "Ajouter le site" : "Enregistrer les changements"}
            </Button>
          </div>
          {!touched && notice}
        </div>

      </form>
    </Container>
  );
}