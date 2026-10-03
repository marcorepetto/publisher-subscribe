#!/usr/bin/env bash

# ==============================================================================
# Script para iniciar 5 consolas independientes para cada suscriptor sísmico
# Ciudades: Arica, Coquimbo, Valparaíso, Concepción, Punta Arenas
# ==============================================================================

# Directorio base del proyecto
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR" || exit 1

# Detectar interprete de Python (usar venv si está activo o existe en la raíz)
if [ -n "$VIRTUAL_ENV" ]; then
    PYTHON_CMD="$VIRTUAL_ENV/bin/python"
elif [ -f "$PROJECT_DIR/venv/bin/python" ]; then
    PYTHON_CMD="$PROJECT_DIR/venv/bin/python"
else
    PYTHON_CMD="python3"
fi

CITIES=("arica" "coquimbo" "valparaiso" "concepcion" "punta_arenas")
CITY_TITLES=("Suscriptor Arica" "Suscriptor Coquimbo" "Suscriptor Valparaíso" "Suscriptor Concepción" "Suscriptor Punta Arenas")

echo "========================================================="
echo "  Lanzando 5 consolas independientes para Suscriptores   "
echo "  Directorio del proyecto: $PROJECT_DIR"
echo "  Python ejecutable: $PYTHON_CMD"
echo "========================================================="

# Detectar emulador de terminal disponible
TERMINAL_EMULATOR=""
if command -v ptyxis >/dev/null 2>&1; then
    TERMINAL_EMULATOR="ptyxis"
elif command -v alacritty >/dev/null 2>&1; then
    TERMINAL_EMULATOR="alacritty"
elif command -v kitty >/dev/null 2>&1; then
    TERMINAL_EMULATOR="kitty"
elif command -v gnome-terminal >/dev/null 2>&1; then
    TERMINAL_EMULATOR="gnome-terminal"
elif command -v konsole >/dev/null 2>&1; then
    TERMINAL_EMULATOR="konsole"
elif command -v xfce4-terminal >/dev/null 2>&1; then
    TERMINAL_EMULATOR="xfce4-terminal"
elif command -v xterm >/dev/null 2>&1; then
    TERMINAL_EMULATOR="xterm"
elif command -v tmux >/dev/null 2>&1; then
    TERMINAL_EMULATOR="tmux"
fi

if [ -z "$TERMINAL_EMULATOR" ]; then
    echo "[ERROR] No se detectó ningún emulador de terminal compatible ni tmux."
    echo "Puedes ejecutar los suscriptores en conjunto con:"
    echo "  $PYTHON_CMD -m subscriber.run_subscribers"
    exit 1
fi

echo "[INFO] Emulador detectado: $TERMINAL_EMULATOR"

# Función para lanzar según el emulador
launch_terminal() {
    local city="$1"
    local title="$2"
    local cmd="cd '$PROJECT_DIR' && '$PYTHON_CMD' -m subscriber.subscriber --city '$city'; echo ''; echo 'Proceso finalizado. Presiona Enter para salir.'; read"

    case "$TERMINAL_EMULATOR" in
        ptyxis)
            ptyxis --new-window --title="$title" -- bash -c "$cmd" &
            ;;
        alacritty)
            alacritty -T "$title" -e bash -c "$cmd" &
            ;;
        kitty)
            kitty --title "$title" bash -c "$cmd" &
            ;;
        gnome-terminal)
            gnome-terminal --title="$title" -- bash -c "$cmd" &
            ;;
        konsole)
            konsole --new-tab -p tabtitle="$title" -e bash -c "$cmd" &
            ;;
        xfce4-terminal)
            xfce4-terminal --title="$title" -e "bash -c \"$cmd\"" &
            ;;
        xterm)
            xterm -title "$title" -e bash -c "$cmd" &
            ;;
        tmux)
            echo "[INFO] Usando tmux para abrir sesiones/paneles..."
            ;;
    esac
}

if [ "$TERMINAL_EMULATOR" = "tmux" ]; then
    SESSION_NAME="sismos_subscribers"
    tmux kill-session -t "$SESSION_NAME" 2>/dev/null
    tmux new-session -d -s "$SESSION_NAME" -n "Arica" "cd '$PROJECT_DIR' && '$PYTHON_CMD' -m subscriber.subscriber --city arica"
    tmux new-window -t "$SESSION_NAME" -n "Coquimbo" "cd '$PROJECT_DIR' && '$PYTHON_CMD' -m subscriber.subscriber --city coquimbo"
    tmux new-window -t "$SESSION_NAME" -n "Valparaiso" "cd '$PROJECT_DIR' && '$PYTHON_CMD' -m subscriber.subscriber --city valparaiso"
    tmux new-window -t "$SESSION_NAME" -n "Concepcion" "cd '$PROJECT_DIR' && '$PYTHON_CMD' -m subscriber.subscriber --city concepcion"
    tmux new-window -t "$SESSION_NAME" -n "PuntaArenas" "cd '$PROJECT_DIR' && '$PYTHON_CMD' -m subscriber.subscriber --city punta_arenas"
    echo "[OK] Sesión de tmux creada: '$SESSION_NAME'. Adjuntando..."
    tmux attach-session -t "$SESSION_NAME"
else
    for i in "${!CITIES[@]}"; do
        city="${CITIES[$i]}"
        title="${CITY_TITLES[$i]}"
        echo " -> Abriendo terminal para: $title ($city)"
        launch_terminal "$city" "$title"
        sleep 0.2
    done
    echo ""
    echo "[OK] 5 consolas abiertas exitosamente para cada suscriptor."
fi
