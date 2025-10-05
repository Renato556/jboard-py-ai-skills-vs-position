from .analysis_controller import AnalysisController

analysis_controller = AnalysisController()
analysis_bp = analysis_controller.blueprint

__all__ = [
    'analysis_bp',
    'AnalysisController'
]
