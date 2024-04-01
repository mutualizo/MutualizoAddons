import requests
import re
import logging
from odoo import models

_logger = logging.getLogger(__name__)

class ZipSearchMixin(models.AbstractModel):
    _name = 'zip.search.mixin'
    _description = 'Pesquisa de CEP'

    def search_address_by_zip(self, zip_code):
        zip_code = re.sub('[^0-9]', '', zip_code or '')
        res = requests.get(f'https://viacep.com.br/ws/{zip_code}/json/')  # noqa

        if not res.ok:
            return {}
        data = res.json()

        state = self.env['res.country.state'].search(
            [('country_id.code', '=', 'BR'),
             ('code', '=', data.get('uf'))])

        city = self.env['res.city'].search([
            ('name', '=ilike', data.get('localidade')),
            ('state_id', '=', state.id)])

        if data.get('logradouro') is None:
            data['logradouro'] = False
        if data.get('bairro') is None:
            data['bairro'] = False

        return {
            'zip': zip_code,
            'street': data['logradouro'],
            'district': data['bairro'],
            'country_id': state.country_id.id,
            'state_id': state.id,
            'city_id': city.id
        }