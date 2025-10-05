import unittest
from unittest.mock import Mock, patch
import requests
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services import OpenAIService


class TestOpenAIService(unittest.TestCase):

    def setUp(self):
        self.service = OpenAIService()

    @patch('services.openai_service.os.getenv')
    def test_init_with_env_variable(self, mock_getenv):
        mock_getenv.return_value = "https://test-api-url.com"
        service = OpenAIService()
        self.assertEqual(service.api_url, "https://test-api-url.com")
        mock_getenv.assert_called_with('OPENAI_API_URL', '')

    @patch('services.openai_service.os.getenv')
    def test_init_without_env_variable(self, mock_getenv):
        mock_getenv.return_value = ''
        service = OpenAIService()
        self.assertEqual(service.api_url, '')

    def test_system_prompt_initialization(self):
        expected_content = ("Você é um assistente de IA e trabalha fazendo match de habilidades com descrição de vagas. "
                          "As habilidades chegam no seguinte formato JSON para você: {\"skills\":[]}, a descrição da vaga chega em formato de texto. "
                          "Responda de maneira resumida com uma porcentagem estimada de match das habilidades do candidato com a vaga e como o candidato pode "
                          "aumentar suas chances de ser selecionado. É EXTREMAMENTE IMPORTANTE QUE SUAS RESPOSTAS SEJAM SEMPRE EM PORTUGUÊS DO BRASIL")

        self.assertEqual(self.service.system_prompt["role"], "system")
        self.assertEqual(self.service.system_prompt["content"], expected_content)

    @patch('services.openai_service.requests.post')
    @patch('builtins.print')
    def test_analyze_match_success(self, mock_print, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "content": "Match de 85% - O candidato tem boa compatibilidade com a vaga."
                    }
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        skills = ["Python", "Flask", "API"]
        description = "Desenvolvedor Python com experiência em Flask"
        api_key = "test-api-key"
        api_url = "https://test-api.com"

        result = self.service.analyze_match(skills, description, api_key, api_url)

        self.assertEqual(result, "Match de 85% - O candidato tem boa compatibilidade com a vaga.")

        expected_payload = {
            "messages": [
                self.service.system_prompt,
                {
                    "role": "user",
                    "content": "Habilidades do candidato: Python, Flask, API\nDescrição da vaga: Desenvolvedor Python com experiência em Flask"
                }
            ],
            "max_completion_tokens": 1000
        }

        mock_post.assert_called_once_with(
            api_url,
            json=expected_payload,
            headers={"Content-Type": "application/json", "api-key": api_key},
            timeout=30
        )

        mock_print.assert_any_call("[OPENAI] Analisando match para 3 habilidades")
        mock_print.assert_any_call("[OPENAI] Análise concluída com sucesso")

    @patch('services.openai_service.requests.post')
    @patch('builtins.print')
    def test_analyze_match_uses_instance_url_when_param_none(self, mock_print, mock_post):
        self.service.api_url = "https://instance-url.com"

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Test response"}}]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        self.service.analyze_match(["Python"], "Test description", "api-key", None)

        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertEqual(args[0], "https://instance-url.com")

    @patch('builtins.print')
    def test_analyze_match_no_api_url_configured(self, mock_print):
        self.service.api_url = ""

        with self.assertRaises(ValueError) as context:
            self.service.analyze_match(["Python"], "Test description", "api-key", None)

        self.assertEqual(str(context.exception), "OPENAI_API_URL não configurada")
        mock_print.assert_called_with("[OPENAI] ERRO: URL da API não configurada")

    @patch('services.openai_service.requests.post')
    @patch('builtins.print')
    def test_analyze_match_http_error(self, mock_print, mock_post):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
        mock_post.return_value = mock_response

        with self.assertRaises(requests.exceptions.HTTPError):
            self.service.analyze_match(["Python"], "Test description", "api-key", "https://test-api.com")

        mock_print.assert_any_call("[OPENAI] ERRO: Status code 404")
        mock_print.assert_any_call("[OPENAI] Response Content: Not Found")

    @patch('services.openai_service.requests.post')
    @patch('builtins.print')
    def test_analyze_match_request_exception(self, mock_print, mock_post):
        request_error = requests.exceptions.RequestException("Connection failed")
        mock_post.side_effect = request_error

        with self.assertRaises(requests.exceptions.RequestException):
            self.service.analyze_match(["Python"], "Test description", "api-key", "https://test-api.com")

        mock_print.assert_any_call(f"[OPENAI] ERRO de requisição: {request_error}")

    @patch('services.openai_service.requests.post')
    @patch('builtins.print')
    def test_analyze_match_invalid_response_no_choices(self, mock_print, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        with self.assertRaises(ValueError) as context:
            self.service.analyze_match(["Python"], "Test description", "api-key", "https://test-api.com")

        self.assertEqual(str(context.exception), "Resposta da OpenAI inválida")
        mock_print.assert_any_call("[OPENAI] ERRO: Resposta inválida da API")

    @patch('services.openai_service.requests.post')
    @patch('builtins.print')
    def test_analyze_match_invalid_response_empty_choices(self, mock_print, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"choices": []}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        with self.assertRaises(ValueError):
            self.service.analyze_match(["Python"], "Test description", "api-key", "https://test-api.com")

    @patch('services.openai_service.requests.post')
    @patch('builtins.print')
    def test_analyze_match_generic_exception(self, mock_print, mock_post):
        mock_post.side_effect = Exception("Unexpected error")

        with self.assertRaises(Exception):
            self.service.analyze_match(["Python"], "Test description", "api-key", "https://test-api.com")

        mock_print.assert_any_call("[OPENAI] ERRO: Unexpected error")

    @patch('services.openai_service.requests.post')
    def test_analyze_match_empty_skills_list(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Candidato precisa desenvolver skills"}}]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        self.service.analyze_match([], "Test description", "api-key", "https://test-api.com")

        call_args = mock_post.call_args
        payload = call_args[1]['json']
        self.assertIn("Habilidades do candidato: ", payload['messages'][1]['content'])

    @patch('services.openai_service.requests.post')
    def test_analyze_match_single_skill(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Match específico para Python"}}]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        self.service.analyze_match(["Python"], "Test description", "api-key", "https://test-api.com")

        call_args = mock_post.call_args
        payload = call_args[1]['json']
        self.assertIn("Habilidades do candidato: Python", payload['messages'][1]['content'])

    @patch('services.openai_service.requests.post')
    def test_analyze_match_special_characters_in_skills(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Análise com acentos"}}]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        skills = ["C++", "C#", "Node.js", "React/Redux"]
        self.service.analyze_match(skills, "Test description", "api-key", "https://test-api.com")

        call_args = mock_post.call_args
        payload = call_args[1]['json']
        self.assertIn("C++, C#, Node.js, React/Redux", payload['messages'][1]['content'])

    @patch('services.openai_service.requests.post')
    def test_analyze_match_long_description(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Análise detalhada"}}]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        long_description = "Lorem ipsum " * 100
        self.service.analyze_match(["Python"], long_description, "api-key", "https://test-api.com")

        call_args = mock_post.call_args
        payload = call_args[1]['json']
        self.assertIn(long_description, payload['messages'][1]['content'])


if __name__ == '__main__':
    unittest.main()
