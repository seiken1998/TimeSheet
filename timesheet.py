import requests
import hashlib
import json

# ====== CONFIGURACIÓN ======
username = "Schinen"
password_raw = "Seiken1998"
dni = "77275361"
timezone = "America/Lima"

# ====== ENCRIPTACIÓN ======
print("🔐 Encriptando contraseña...")
password_md5 = hashlib.md5(password_raw.encode()).hexdigest()

# ====== LOGIN ======
login_url = "https://empleados.sapiensconsultingperu.com/api/api/Auth/Login"
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9,es;q=0.8,ja;q=0.7',
    'Content-Type': 'application/json',
    'Origin': 'https://empleados.sapiensconsultingperu.com',
    'Referer': 'https://empleados.sapiensconsultingperu.com/portal/',
    'User-Agent': 'Mozilla/5.0'
}
login_data = {
    "Username": username,
    "Password": password_md5
}

print("➡️ Iniciando sesión...")
response = requests.post(login_url, headers=headers, json=login_data)

if response.status_code == 200:
    login_result = response.json()
    if login_result.get("Code") == 200:
        print("✅ Login exitoso.")
        token = login_result["Objeto"]["AccessToken"]
        user_id = login_result["Objeto"]["Id"]

        # ====== REGISTRO DE ASISTENCIA ======
        punch_url = "https://empleados.sapiensconsultingperu.com/api/api/TimeRecord/"
        punch_headers = headers.copy()
        punch_headers['Authorization'] = f"Bearer {token}"

        punch_data = {
            "UserId": user_id,
            "TimeZone": timezone,
            "Dni": dni
        }

        print("🕐 Registrando asistencia...")
        punch_response = requests.post(punch_url, headers=punch_headers, json=punch_data)

        if punch_response.status_code == 200:
            punch_result = punch_response.json()
            if punch_result.get("Code") == 200:
                print("✅ Asistencia registrada correctamente.")
            else:
                print(f"⚠️ No se pudo registrar asistencia: {punch_result.get('Message')}")
        else:
            print(f"❌ Error HTTP al registrar asistencia: {punch_response.status_code}")
    else:
        print(f"❌ Error de login: {login_result.get('Message')}")
else:
    print(f"❌ Error HTTP al iniciar sesión: {response.status_code}")
