import os
import subprocess
import threading
from datetime import datetime

def inicializador_backup(bancos, sqlpackage_path, credenciais, pasta_destino, log_callback, on_finish_callback):
    def processamento():
        data = datetime.now().strftime("%Y-%m-%d")

        for banco in bancos:
            log_callback(f"Extraindo {banco}...", "info")
            destino = os.path.join(pasta_destino, f"{banco}_{data}.bacpac")

            comando = [
                sqlpackage_path,
                "/Action:Export",
                f"/SourceServerName:{credenciais['host']}",
                f"/SourceDatabaseName:{banco}",
                f"/SourceUser:{credenciais['user']}",
                f"/SourcePassword:{credenciais['pass']}",
                f"/TargetFile:{destino}"
            ]

            try:
                resultado = subprocess.run(
                    comando,
                    capture_output=True,
                    text=True,
                    creationflags=(subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
                )

                if resultado.returncode == 0:
                    log_callback(f"{banco} exportado com sucesso.", "success")
                else:
                    log_callback(f"Erro ao exportar {banco}", "error")
                    log_callback(resultado.stderr, "warning")

            except Exception as e:
                log_callback(str(e), "error")

        log_callback("Processo finalizado.", "success")
        on_finish_callback()

    thread = threading.Thread(target=processamento)
    thread.start()