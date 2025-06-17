try:
    import psycopg2
except ImportError as e:
    raise ImportError("O módulo 'psycopg2' não está instalado. Instale-o com 'pip install psycopg2-binary'.") from e

from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter
from logging_config import get_logger
from crudTurma import turmas_bp

logger = get_logger(__name__)

app = Flask(__name__)

# Configuração do Prometheus
metrics = PrometheusMetrics(app, default_labels={'app_name': 'flask_app'})

# Métricas personalizadas para sucessos e erros
success_counter = Counter(
    'http_success_count', 'Contagem de respostas HTTP com sucesso',
    ['endpoint', 'method', 'status']
)

error_counter = Counter(
    'http_error_count', 'Contagem de respostas HTTP com erro',
    ['endpoint', 'method', 'status']
)

@app.after_request
def after_request(response):
    """
    Middleware para capturar os retornos de todos os endpoints.
    """
    endpoint = request.path
    method = request.method
    status = response.status_code

    if 200 <= status < 300:
        success_counter.labels(endpoint=endpoint, method=method, status=str(status)).inc()
    else:
        error_counter.labels(endpoint=endpoint, method=method, status=str(status)).inc()

    return response

# Registro do Blueprint
app.register_blueprint(turmas_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
