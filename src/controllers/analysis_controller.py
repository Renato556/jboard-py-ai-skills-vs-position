from flask import Blueprint, request, jsonify, current_app
from src.services import AnalysisService
from src.models import AnalysisRequest, ErrorResponse
import requests


class AnalysisController:

    def __init__(self):
        self.analysis_service = AnalysisService()
        self.blueprint = self._create_blueprint()

    def _create_blueprint(self) -> Blueprint:
        bp = Blueprint('analysis', __name__)
        bp.add_url_rule('/analyse', 'analyse_position', self.analyse_position, methods=['POST'])
        bp.add_url_rule('/health', 'health_check', self.health_check, methods=['GET'])
        return bp

    def analyse_position(self):
        try:
            data = request.get_json()
            if not data:
                error = ErrorResponse("JSON não fornecido")
                return jsonify(error.to_dict()), 400

            if 'position' not in data:
                error = ErrorResponse("Campo position é obrigatório")
                return jsonify(error.to_dict()), 400

            api_key = current_app.config.get('OPENAI_API_KEY')
            if not api_key:
                error = ErrorResponse("API key da OpenAI não configurada")
                return jsonify(error.to_dict()), 500

            api_url = current_app.config.get('OPENAI_API_URL')
            if not api_url:
                error = ErrorResponse("URL da API OpenAI não configurada")
                return jsonify(error.to_dict()), 500

            analysis_request = AnalysisRequest.from_dict(data)
            result = self.analysis_service.analyze_position(analysis_request, api_key, api_url)

            return jsonify(result), 200

        except requests.exceptions.RequestException as e:
            print(f"[CONTROLLER] ERRO de requisição: {str(e)}")
            error = ErrorResponse(f"Erro ao acessar a URL: {str(e)}")
            return jsonify(error.to_dict()), 500

        except ValueError as e:
            print(f"[CONTROLLER] ERRO de validação: {str(e)}")
            error = ErrorResponse(str(e))
            return jsonify(error.to_dict()), 404

        except Exception as e:
            print(f"[CONTROLLER] ERRO: {str(e)}")
            error = ErrorResponse("Erro interno do servidor")
            return jsonify(error.to_dict()), 500

    def health_check(self):
        return jsonify({'status': 'OK'}), 200
