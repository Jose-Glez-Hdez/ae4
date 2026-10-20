import os
import socket

from django.conf import settings
from django.db import connection
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.utils.html import escape
from django.views.decorators.http import require_POST


def _json(datos, status=200):
    return JsonResponse(datos, status=status, json_dumps_params={"ensure_ascii": False})


def _mensaje():
    return os.environ.get("APP_MENSAJE", "Hola, esto es un mensaje de ejemplo.")


def inicio(request):
    """Página HTML generada por Django (se sirve a través de nginx)."""
    html = f"""<!doctype html>
<html lang="es">
<head><meta charset="utf-8"><title>Aplicación DPL — UT4</title></head>
<body>
  <h1>Aplicación DPL — UT4</h1>
  <p>{escape(_mensaje())}</p>
  <p>Servidor de aplicaciones: <code>{escape(socket.gethostname())}</code></p>
  <ul>
    <li><a href="/healthz">/healthz</a></li>
    <li><a href="/api/mensaje">/api/mensaje</a></li>
    <li><a href="/api/visitas">/api/visitas</a></li>
    <li><a href="/api/lugares">/api/lugares</a></li>
  </ul>
</body>
</html>
"""
    return HttpResponse(html)


def healthz(request):
    return _json({"status": "ok"})


def mensaje(request):
    return _json({
        "mensaje": _mensaje(),
        "hostname": socket.gethostname(),
        "fecha": timezone.localtime().isoformat(timespec="seconds"),
    })


def visitas(request):
    carpeta = settings.APP_DATA_DIR
    carpeta.mkdir(parents=True, exist_ok=True)
    fichero = carpeta / "visitas.txt"
    try:
        total = int(fichero.read_text().strip() or 0)
    except FileNotFoundError:
        total = 0
    total += 1
    fichero.write_text(f"{total}\n")
    return _json({"visitas": total})


def lugares(request):
    if not settings.DB_HOST:
        return _json({"error": "Base de datos no configurada (falta DB_HOST)"}, status=503)
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, name, visited FROM places ORDER BY id")
            filas = cursor.fetchall()
    except Exception as exc:  
        return _json({"error": f"No se pudo consultar la base de datos: {exc}"}, status=503)
    datos = [{"id": i, "name": nombre, "visited": visitado} for i, nombre, visitado in filas]
    return _json({"lugares": datos, "total": len(datos)})


@require_POST
def login(request):
    host = os.environ.get("LDAP_HOST", "")
    if not host:
        return _json({"error": "Directorio LDAP no configurado (falta LDAP_HOST)"}, status=503)

    from ldap3 import Connection, Server

    usuario = request.POST.get("usuario", "")
    password = request.POST.get("password", "")
    base_dn = os.environ.get("LDAP_BASE_DN", "dc=dpl,dc=local")
    user_dn = f"uid={usuario},ou=people,{base_dn}"
    if not usuario or not password:
        return _json({"error": "Faltan usuario o contraseña"}, status=401)
    try:
        conexion = Connection(Server(host, connect_timeout=3), user=user_dn, password=password)
        if not conexion.bind():
            return _json({"error": "Credenciales incorrectas"}, status=401)
        conexion.unbind()
    except Exception as exc:
        return _json({"error": f"No se pudo contactar con el directorio: {exc}"}, status=503)
    return _json({"usuario": usuario, "dn": user_dn})