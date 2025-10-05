from .app_config import Config, DevelopmentConfig, ProductionConfig

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

__all__ = [
    'Config',
    'DevelopmentConfig',
    'ProductionConfig',
    'config'
]
