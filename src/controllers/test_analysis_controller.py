import unittest
from unittest.mock import Mock, patch
import json
from flask import Flask
import requests

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.controllers.analysis_controller import AnalysisController


class TestAnalysisController(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['OPENAI_API_KEY'] = 'test_api_key'
        self.app.config['OPENAI_API_URL'] = 'https://test-openai-url.com'

        self.controller = AnalysisController()
        self.app.register_blueprint(self.controller.blueprint)
        self.client = self.app.test_client()

        self.mock_analysis_service = Mock()
        self.controller.analysis_service = self.mock_analysis_service

    def test_init_creates_blueprint(self):
        controller = AnalysisController()
        self.assertIsNotNone(controller.blueprint)
        self.assertEqual(controller.blueprint.name, 'analysis')

    def test_create_blueprint_adds_routes(self):
        controller = AnalysisController()
        blueprint = controller._create_blueprint()

        self.assertEqual(blueprint.name, 'analysis')
        test_app = Flask(__name__)
        test_app.register_blueprint(blueprint)

        with test_app.app_context():
            rules = [rule.rule for rule in test_app.url_map.iter_rules()]
            self.assertIn('/analyse', rules)
            self.assertIn('/health', rules)

    def test_health_check_returns_ok(self):
        with self.app.app_context():
            response = self.controller.health_check()
            data, status_code = response

            self.assertEqual(status_code, 200)
            self.assertEqual(data.get_json(), {'status': 'OK'})

    def test_analyse_position_success(self):
        self.mock_analysis_service.analyze_position.return_value = {
            "message": "Match de 85% - Candidato tem boa compatibilidade"
        }

        test_data = {
            "position": "https://example.com/job",
            "skills": ["Python", "Flask", "API"]
        }

        with self.app.app_context():
            response = self.client.post('/analyse',
                                      data=json.dumps(test_data),
                                      content_type='application/json')

            self.assertEqual(response.status_code, 200)
            response_data = json.loads(response.data)
            self.assertEqual(response_data["message"], "Match de 85% - Candidato tem boa compatibilidade")

            self.mock_analysis_service.analyze_position.assert_called_once()
            call_args = self.mock_analysis_service.analyze_position.call_args
            self.assertEqual(call_args[0][1], 'test_api_key')
            self.assertEqual(call_args[0][2], 'https://test-openai-url.com')

    def test_analyse_position_no_json(self):
        with self.app.app_context():
            response = self.client.post('/analyse')

            self.assertEqual(response.status_code, 500)
            response_data = json.loads(response.data)
            self.assertEqual(response_data['error'], 'Erro interno do servidor')

    def test_analyse_position_missing_position_field(self):
        test_data = {
            "skills": ["Python", "Flask"]
        }

        with self.app.app_context():
            response = self.client.post('/analyse',
                                      data=json.dumps(test_data),
                                      content_type='application/json')

            self.assertEqual(response.status_code, 400)
            response_data = json.loads(response.data)
            self.assertEqual(response_data['error'], 'Campo position é obrigatório')

    def test_analyse_position_missing_api_key(self):
        self.app.config['OPENAI_API_KEY'] = None

        test_data = {
            "position": "https://example.com/job",
            "skills": ["Python"]
        }

        with self.app.app_context():
            response = self.client.post('/analyse',
                                      data=json.dumps(test_data),
                                      content_type='application/json')

            self.assertEqual(response.status_code, 500)
            response_data = json.loads(response.data)
            self.assertEqual(response_data['error'], 'API key da OpenAI não configurada')

    def test_analyse_position_missing_api_url(self):
        self.app.config['OPENAI_API_URL'] = None

        test_data = {
            "position": "https://example.com/job",
            "skills": ["Python"]
        }

        with self.app.app_context():
            response = self.client.post('/analyse',
                                      data=json.dumps(test_data),
                                      content_type='application/json')

            self.assertEqual(response.status_code, 500)
            response_data = json.loads(response.data)
            self.assertEqual(response_data['error'], 'URL da API OpenAI não configurada')

    def test_analyse_position_request_exception(self):
        self.mock_analysis_service.analyze_position.side_effect = requests.exceptions.RequestException("Connection error")

        test_data = {
            "position": "https://example.com/job",
            "skills": ["Python"]
        }

        with self.app.app_context():
            response = self.client.post('/analyse',
                                      data=json.dumps(test_data),
                                      content_type='application/json')

            self.assertEqual(response.status_code, 500)
            response_data = json.loads(response.data)
            self.assertEqual(response_data['error'], 'Erro ao acessar a URL: Connection error')

    def test_analyse_position_value_error(self):
        self.mock_analysis_service.analyze_position.side_effect = ValueError("URL inválida")

        test_data = {
            "position": "invalid-url",
            "skills": ["Python"]
        }

        with self.app.app_context():
            response = self.client.post('/analyse',
                                      data=json.dumps(test_data),
                                      content_type='application/json')

            self.assertEqual(response.status_code, 404)
            response_data = json.loads(response.data)
            self.assertEqual(response_data['error'], 'URL inválida')

    def test_analyse_position_generic_exception(self):
        self.mock_analysis_service.analyze_position.side_effect = Exception("Erro interno")

        test_data = {
            "position": "https://example.com/job",
            "skills": ["Python"]
        }

        with self.app.app_context():
            response = self.client.post('/analyse',
                                      data=json.dumps(test_data),
                                      content_type='application/json')

            self.assertEqual(response.status_code, 500)
            response_data = json.loads(response.data)
            self.assertEqual(response_data['error'], 'Erro interno do servidor')

    def test_analyse_position_empty_skills(self):
        self.mock_analysis_service.analyze_position.return_value = {
            "message": "Candidato precisa desenvolver skills específicas"
        }

        test_data = {
            "position": "https://example.com/job",
            "skills": []
        }

        with self.app.app_context():
            response = self.client.post('/analyse',
                                      data=json.dumps(test_data),
                                      content_type='application/json')

            self.assertEqual(response.status_code, 200)
            response_data = json.loads(response.data)
            self.assertEqual(response_data["message"], "Candidato precisa desenvolver skills específicas")

    def test_analyse_position_with_special_characters(self):
        self.mock_analysis_service.analyze_position.return_value = {
            "message": "Análise com acentos e ç"
        }

        test_data = {
            "position": "https://example.com/job",
            "skills": ["Python", "C++", "C#"]
        }

        with self.app.app_context():
            response = self.client.post('/analyse',
                                      data=json.dumps(test_data),
                                      content_type='application/json')

            self.assertEqual(response.status_code, 200)
            response_data = json.loads(response.data)
            self.assertEqual(response_data["message"], "Análise com acentos e ç")

    @patch('builtins.print')
    def test_analyse_position_prints_errors(self, mock_print):
        self.mock_analysis_service.analyze_position.side_effect = ValueError("Erro de teste")

        test_data = {
            "position": "https://example.com/job",
            "skills": ["Python"]
        }

        with self.app.app_context():
            response = self.client.post('/analyse',
                                      data=json.dumps(test_data),
                                      content_type='application/json')

            mock_print.assert_called_with('[CONTROLLER] ERRO de validação: Erro de teste')
            self.assertEqual(response.status_code, 404)

    def test_blueprint_routes_configuration(self):
        with self.app.app_context():
            response = self.client.get('/health')
            self.assertEqual(response.status_code, 200)

            response = self.client.post('/health')
            self.assertEqual(response.status_code, 405)

            response = self.client.get('/analyse')
            self.assertEqual(response.status_code, 405)

if __name__ == '__main__':
    unittest.main()
