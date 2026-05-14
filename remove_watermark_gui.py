#!/usr/bin/env python3
"""
Veo Watermark Remover — Interfaz gráfica
-----------------------------------------
Ventana para elegir el video de entrada y el destino de salida,
con barra de progreso en tiempo real.

Requisito: FFmpeg instalado en el sistema.
"""

import subprocess
import threading
import re
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path


DELOGO_FILTER = "delogo=x=2190:y=1308:w=355:h=118:show=0"

WINDOW_TITLE = "Veo Watermark Remover"
WINDOW_WIDTH = 560
WINDOW_HEIGHT = 280


def check_ffmpeg():
    try:
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False


def get_duration_seconds(input_path: str) -> float:
    """Devuelve la duración del video en segundos usando ffprobe."""
    try:
        result = subprocess.run(
            [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                input_path,
            ],
            capture_output=True, text=True,
        )
        return float(result.stdout.strip())
    except Exception:
        return 0.0


def parse_time_seconds(line: str) -> float | None:
    """Extrae el tiempo actual de una línea de salida de FFmpeg."""
    match = re.search(r"time=(\d+):(\d+):(\d+\.\d+)", line)
    if match:
        h, m, s = match.groups()
        return int(h) * 3600 + int(m) * 60 + float(s)
    return None


class WatermarkRemoverApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.resizable(False, False)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self._center_window()
        self._build_ui()

    def _center_window(self):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - WINDOW_WIDTH) // 2
        y = (self.root.winfo_screenheight() - WINDOW_HEIGHT) // 2
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")

    def _build_ui(self):
        pad = {"padx": 16, "pady": 6}

        # --- Entrada ---
        tk.Label(self.root, text="Video de entrada:", anchor="w").pack(fill="x", padx=16, pady=(16, 0))
        row_in = tk.Frame(self.root)
        row_in.pack(fill="x", **pad)
        self.input_var = tk.StringVar()
        tk.Entry(row_in, textvariable=self.input_var, state="readonly", width=52).pack(side="left", fill="x", expand=True)
        tk.Button(row_in, text="Elegir", width=8, command=self._choose_input).pack(side="left", padx=(6, 0))

        # --- Salida ---
        tk.Label(self.root, text="Guardar como:", anchor="w").pack(fill="x", padx=16, pady=(4, 0))
        row_out = tk.Frame(self.root)
        row_out.pack(fill="x", **pad)
        self.output_var = tk.StringVar()
        tk.Entry(row_out, textvariable=self.output_var, state="readonly", width=52).pack(side="left", fill="x", expand=True)
        tk.Button(row_out, text="Elegir", width=8, command=self._choose_output).pack(side="left", padx=(6, 0))

        # --- Progreso ---
        progress_frame = tk.Frame(self.root)
        progress_frame.pack(fill="x", padx=16, pady=(10, 0))
        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = ttk.Progressbar(
            progress_frame, variable=self.progress_var, maximum=100, length=520
        )
        self.progress_bar.pack(fill="x")
        self.status_var = tk.StringVar(value="")
        tk.Label(self.root, textvariable=self.status_var, anchor="w", fg="#555555").pack(fill="x", padx=16)

        # --- Botón principal ---
        self.run_button = tk.Button(
            self.root,
            text="Quitar marca de agua",
            font=("", 13, "bold"),
            bg="#1a73e8", fg="white",
            activebackground="#1558b0", activeforeground="white",
            relief="flat", cursor="hand2",
            padx=20, pady=8,
            command=self._start_processing,
        )
        self.run_button.pack(pady=(12, 16))

    # ------------------------------------------------------------------
    # Selección de archivos
    # ------------------------------------------------------------------

    def _choose_input(self):
        path = filedialog.askopenfilename(
            title="Elige el video de entrada",
            filetypes=[("Videos MP4", "*.mp4"), ("Todos los archivos", "*.*")],
        )
        if not path:
            return
        self.input_var.set(path)
        # Auto-completar salida si está vacía
        if not self.output_var.get():
            p = Path(path)
            self.output_var.set(str(p.parent / f"{p.stem}_sin_marca{p.suffix}"))

    def _choose_output(self):
        initial = self.output_var.get() or self.input_var.get() or ""
        p = Path(initial) if initial else Path.home()
        path = filedialog.asksaveasfilename(
            title="Guardar video procesado",
            initialdir=str(p.parent),
            initialfile=p.name if initial else "video_sin_marca.mp4",
            defaultextension=".mp4",
            filetypes=[("Videos MP4", "*.mp4")],
        )
        if path:
            self.output_var.set(path)

    # ------------------------------------------------------------------
    # Procesamiento
    # ------------------------------------------------------------------

    def _start_processing(self):
        input_path = self.input_var.get().strip()
        output_path = self.output_var.get().strip()

        if not input_path:
            messagebox.showerror("Error", "Por favor elige un video de entrada.")
            return
        if not Path(input_path).exists():
            messagebox.showerror("Error", "No se encontró el archivo seleccionado.")
            return
        if not output_path:
            messagebox.showerror("Error", "Por favor elige dónde guardar el resultado.")
            return
        if not check_ffmpeg():
            messagebox.showerror(
                "FFmpeg no encontrado",
                "FFmpeg no está instalado.\n\n"
                "Mac:     brew install ffmpeg\n"
                "Windows: winget install ffmpeg",
            )
            return

        self.run_button.config(state="disabled")
        self.progress_var.set(0)
        self.status_var.set("Iniciando...")

        threading.Thread(
            target=self._run_ffmpeg,
            args=(input_path, output_path),
            daemon=True,
        ).start()

    def _run_ffmpeg(self, input_path: str, output_path: str):
        duration = get_duration_seconds(input_path)

        cmd = [
            "ffmpeg", "-y",
            "-i", input_path,
            "-vf", DELOGO_FILTER,
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "18",
            "-c:a", "copy",
            output_path,
        ]

        try:
            process = subprocess.Popen(
                cmd,
                stderr=subprocess.PIPE,
                stdout=subprocess.DEVNULL,
                text=True,
                bufsize=1,
            )

            for line in process.stderr:
                elapsed = parse_time_seconds(line)
                if elapsed is not None and duration > 0:
                    pct = min(elapsed / duration * 100, 99)
                    remaining = max(duration - elapsed, 0)
                    self.root.after(0, self._update_progress, pct, remaining)

            process.wait()
            success = process.returncode == 0
        except Exception:
            success = False

        self.root.after(0, self._on_finish, success, output_path)

    def _update_progress(self, pct: float, remaining_secs: float):
        self.progress_var.set(pct)
        mins = int(remaining_secs) // 60
        secs = int(remaining_secs) % 60
        if mins > 0:
            self.status_var.set(f"Procesando... (~{mins} min {secs} s restantes)")
        else:
            self.status_var.set(f"Procesando... (~{secs} s restantes)")

    def _on_finish(self, success: bool, output_path: str):
        self.run_button.config(state="normal")
        if success:
            self.progress_var.set(100)
            self.status_var.set("Listo.")
            messagebox.showinfo(
                "Completado",
                f"Video guardado en:\n{output_path}",
            )
        else:
            self.progress_var.set(0)
            self.status_var.set("Error al procesar el video.")
            messagebox.showerror(
                "Error",
                "Error al procesar el video.\nRevisa que el archivo no esté dañado.",
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = WatermarkRemoverApp(root)
    root.mainloop()
