import requests
import os
from dotenv import load_dotenv

load_dotenv()


class OpenAIService:

    def __init__(self):
        self.api_url = os.getenv('OPENAI_API_URL', '')
        self.system_prompt = {
            "role": "system",
            "content": "Você é um assistente de IA e trabalha fazendo match de habilidades com descrição de vagas. As habilidades chegam no seguinte formato JSON para você: {\"skills\":[]}, a descrição da vaga chega em formato de texto. Responda de maneira resumida com uma porcentagem estimada de match das habilidades do candidato com a vaga e como o candidato pode aumentar suas chances de ser selecionado. É EXTREMAMENTE IMPORTANTE QUE SUAS RESPOSTAS SEJAM SEMPRE EM PORTUGUÊS DO BRASIL"
        }

    def analyze_match(self, skills: list, description: str, api_key: str, api_url: str = None) -> str:
        url_to_use = api_url or self.api_url

        if not url_to_use:
            print(f"[OPENAI] ERRO: URL da API não configurada")
            raise ValueError("OPENAI_API_URL não configurada")

        skills_text = ", ".join(skills)
        user_content = f"Habilidades do candidato: {skills_text}\nDescrição da vaga: {description}"

        print(f"[OPENAI] Analisando match para {len(skills)} habilidades")

        payload = {
            "messages": [
                self.system_prompt,
                {
                    "role": "user",
                    "content": user_content
                }
            ],
            "max_completion_tokens": 1000
        }

        try:
            response = requests.post(url_to_use, json=payload, headers={"Content-Type": "application/json", "api-key": api_key}, timeout=30)

            if response.status_code != 200:
                print(f"[OPENAI] ERRO: Status code {response.status_code}")
                print(f"[OPENAI] Response Content: {response.text}")

            response.raise_for_status()
            result = response.json()

            if "choices" not in result or not result["choices"]:
                print(f"[OPENAI] ERRO: Resposta inválida da API")
                raise ValueError("Resposta da OpenAI inválida")

            ai_message = result["choices"][0]["message"]["content"]
            print(f"[OPENAI] Análise concluída com sucesso")

            return ai_message

        except requests.exceptions.HTTPError as e:
            print(f"[OPENAI] ERRO HTTP: {e}")
            raise
        except requests.exceptions.RequestException as e:
            print(f"[OPENAI] ERRO de requisição: {e}")
            raise
        except Exception as e:
            print(f"[OPENAI] ERRO: {e}")
            raise
