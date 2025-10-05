import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services import TextProcessingService


class TestTextProcessingService(unittest.TestCase):

    def setUp(self):
        self.service = TextProcessingService()

    def test_format_description_basic_text(self):
        text = "Este é um texto simples."
        result = TextProcessingService.format_description(text)
        self.assertEqual(result, "Este é um texto simples.")

    def test_format_description_multiple_spaces(self):
        text = "Este    é   um    texto  com     espaços    múltiplos."
        result = TextProcessingService.format_description(text)
        self.assertEqual(result, "Este é um texto com espaços múltiplos.")

    def test_format_description_tabs_and_newlines(self):
        text = "Este\té\num\ntexto\rcom\r\ntabs\te\nquebras\rde\nlinha."
        result = TextProcessingService.format_description(text)
        self.assertEqual(result, "Este é um texto com tabs e quebras de linha.")

    def test_format_description_leading_trailing_spaces(self):
        text = "   Este é um texto com espaços no início e fim   "
        result = TextProcessingService.format_description(text)
        self.assertEqual(result, "Este é um texto com espaços no início e fim")

    def test_format_description_mixed_whitespace(self):
        text = "\t\n  Este\t\té\n\rum\r\ntexto\t\tcom\n\nvários\r\rtipos\t\nde\r\nespaços  \n\t"
        result = TextProcessingService.format_description(text)
        self.assertEqual(result, "Este é um texto com vários tipos de espaços")

    def test_format_description_empty_string(self):
        text = ""
        result = TextProcessingService.format_description(text)
        self.assertEqual(result, "")

    def test_format_description_only_whitespace(self):
        text = "   \t\n\r   "
        result = TextProcessingService.format_description(text)
        self.assertEqual(result, "")

    def test_format_description_single_word(self):
        text = "palavra"
        result = TextProcessingService.format_description(text)
        self.assertEqual(result, "palavra")

    def test_format_description_single_word_with_spaces(self):
        text = "   palavra   "
        result = TextProcessingService.format_description(text)
        self.assertEqual(result, "palavra")

    def test_format_description_html_like_content(self):
        text = "Desenvolvedor\n\nPython\t\tcom experiência\r\nem\n\nFlask\te\rDjango."
        result = TextProcessingService.format_description(text)
        self.assertEqual(result, "Desenvolvedor Python com experiência em Flask e Django.")

    def test_format_description_special_characters(self):
        text = "Descrição   com\nç,\tá,\ré,\nã\te\routros\nacentos."
        result = TextProcessingService.format_description(text)
        self.assertEqual(result, "Descrição com ç, á, é, ã e outros acentos.")

    def test_format_description_numbers_and_symbols(self):
        text = "Salário:   R$\t5.000,00\n-\rR$\n8.000,00\tcom\nbenefícios."
        result = TextProcessingService.format_description(text)
        self.assertEqual(result, "Salário: R$ 5.000,00 - R$ 8.000,00 com benefícios.")

    def test_format_description_unicode_characters(self):
        text = "Empresa\n\n🚀\ttech\tcom\r\ncultura\t\t💡\tinovadora."
        result = TextProcessingService.format_description(text)
        self.assertEqual(result, "Empresa 🚀 tech com cultura 💡 inovadora.")

    def test_format_description_very_long_text(self):
        text = "Lorem\n\nipsum\t\tdolor\r\rsit\namet,\tconsectetur\r\nadipiscing\telit.\nSed\tdo\reiusmod\n\ntempor\t\tincididunt\r\rut\nlabore\tet\rdolore\n\nmagna\t\taliqua."
        result = TextProcessingService.format_description(text)
        expected = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
        self.assertEqual(result, expected)

    def test_format_description_consecutive_newlines(self):
        text = "Primeira linha\n\n\n\nSegunda linha\n\n\nTerceira linha"
        result = TextProcessingService.format_description(text)
        self.assertEqual(result, "Primeira linha Segunda linha Terceira linha")

    def test_format_description_mixed_spaces_and_content(self):
        text = "   Python   \n\n   Flask   \t\t   API   \r\r   REST   "
        result = TextProcessingService.format_description(text)
        self.assertEqual(result, "Python Flask API REST")

    def test_format_description_static_method(self):
        text = "  Teste   método\t\testático  "
        result = TextProcessingService.format_description(text)
        self.assertEqual(result, "Teste método estático")

    def test_format_description_preserves_single_spaces(self):
        text = "Palavra1 palavra2 palavra3"
        result = TextProcessingService.format_description(text)
        self.assertEqual(result, "Palavra1 palavra2 palavra3")


if __name__ == '__main__':
    unittest.main()
