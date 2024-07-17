from mitmproxy import http

blocked_domains = ["queue-it.net"]

def request(flow: http.HTTPFlow) -> None:
    for domain in blocked_domains:
        if domain in flow.request.pretty_host:
            flow.response = http.HTTPResponse.make(
                403,  # Código de estado HTTP
                "Esta URL está bloqueada por el proxy.".encode('utf-8'),  # Cuerpo del mensaje
                {"Content-Type": "text/html"}  # Tipo de contenido
            )
