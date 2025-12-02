import tkinter as tk
from tkinter import ttk, messagebox
from motor_inferencia import MotorInferencia
import os

# --- 1. Configuración y Mapeo de Datos ---

# Copiamos el mapeo actualizado incluyendo los diferenciales
MAPEO_HECHOS = {
    1: "fiebre_alta",
    2: "tos",
    3: "coriza",
    4: "conjuntivitis",
    5: "koplik",
    6: "exantema",
    7: "contacto_sospechoso",
    8: "vacunado",
    9: "fiebre_baja",
    10: "adenopatia_retroauricular",
    11: "fiebre_alta_desaparece",
    12: "exantema_posterior",
    13: "faringitis",
    14: "exantema_tipo_lija"
}

class SistemaExpertoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Experto: Diagnóstico Exantemático")
        self.root.geometry("850x800")
        
        # Obtiene la carpeta donde está ESTE archivo script
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        # Une la carpeta con el nombre del archivo
        ruta_json = os.path.join(directorio_actual, "sarampion_db.json")
        
        # Inicializar motor usando la ruta completa
        try:
            self.motor = MotorInferencia(ruta_json) # <--- Usar ruta_json aquí
            self.preguntas = self.motor.data["questions"]
        except Exception as e:
            # Esto te dirá exactamente qué pasa (si es ruta o error de sintaxis)
            messagebox.showerror("Error Crítico", f"Detalle del error:\n{e}")
            self.root.destroy()
            return

        # Diccionario para guardar las variables de respuesta (IntVars: 1=Sí, 0=No)
        self.respuestas_vars = {}

        self._crear_interfaz()

    def _crear_interfaz(self):
        # --- Estilos ---
        style = ttk.Style()
        style.configure("TLabel", font=("Helvetica", 11))
        style.configure("Title.TLabel", font=("Helvetica", 16, "bold"), foreground="#2c3e50")
        style.configure("Question.TLabel", font=("Helvetica", 10))

        # --- Encabezado ---
        header_frame = ttk.Frame(self.root, padding="20 20 20 10")
        header_frame.pack(fill=tk.X)
        
        lbl_titulo = ttk.Label(header_frame, text="Encuesta de Diagnóstico para Sarampión\no posibles enfermedades Exantemáticas", style="Title.TLabel")
        lbl_titulo.pack(anchor=tk.W)
        
        lbl_instrucciones = ttk.Label(header_frame, text="Seleccione los síntomas presentes en el paciente:", foreground="gray")
        lbl_instrucciones.pack(anchor=tk.W, pady=(2,0))

        # --- Área de Preguntas (con Scroll) ---
        canvas = tk.Canvas(self.root)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, padding="20")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # --- Generación Dinámica de Preguntas ---
        # Agrupamos visualmente para facilitar la lectura del médico
        self._agregar_seccion(scrollable_frame, "Signos Vitales y Generales")
        
        for p in self.preguntas:
            # Crear contenedor para cada pregunta
            q_frame = ttk.Frame(scrollable_frame, padding="0 5 0 5")
            q_frame.pack(fill=tk.X, pady=2)

            # Texto de la pregunta
            lbl = ttk.Label(q_frame, text=f"{p['id']}. {p['text']}", style="Question.TLabel", wraplength=450)
            lbl.pack(side=tk.LEFT, padx=(0, 10))

            # Contenedor de opciones (Radiobuttons)
            opt_frame = ttk.Frame(q_frame)
            opt_frame.pack(side=tk.RIGHT)

            var = tk.IntVar(value=0) # Por defecto NO (evita falsos positivos por olvido)
            self.respuestas_vars[p['id']] = var

            r_si = ttk.Radiobutton(opt_frame, text="SÍ", variable=var, value=1)
            r_no = ttk.Radiobutton(opt_frame, text="NO", variable=var, value=0)
            
            r_si.pack(side=tk.LEFT, padx=5)
            r_no.pack(side=tk.LEFT, padx=5)
            
            # Separador visual cada 5 preguntas para no cansar la vista
            if p['id'] % 5 == 0:
                ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', pady=10)

        # --- Botón de Acción ---
        btn_frame = ttk.Frame(self.root, padding="20")
        btn_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        btn_diagnosticar = ttk.Button(btn_frame, text="Generar Diagnóstico", command=self.realizar_diagnostico)
        btn_diagnosticar.pack(fill=tk.X, ipady=10)

    def _agregar_seccion(self, parent, titulo):
        lbl = ttk.Label(parent, text=titulo, font=("Helvetica", 12, "bold"), foreground="#34495e")
        lbl.pack(anchor="w", pady=(10, 5))
        ttk.Separator(parent, orient='horizontal').pack(fill='x', pady=(0, 10))

    def realizar_diagnostico(self):
        # 1. Limpiar hechos anteriores del motor
        self.motor.facts = set()
        hechos_recolectados = []

        # 2. Recolectar respuestas de la GUI
        for id_pregunta, var in self.respuestas_vars.items():
            if var.get() == 1: # Si el usuario marcó SÍ
                hecho = MAPEO_HECHOS.get(id_pregunta)
                if hecho:
                    self.motor.agregar_hecho(hecho)
                    hechos_recolectados.append(hecho)

        # 3. Lógica Especial (Normalización OR para síntomas respiratorios)
        # Verifica si existe alguno de los tres en los hechos recolectados
        sintomas_resp = {"tos", "coriza", "conjuntivitis"}
        if not sintomas_resp.isdisjoint(self.motor.facts):
            self.motor.agregar_hecho("tos_o_coriza_o_conjuntivitis")

        # 4. Inferir
        conclusiones = self.motor.inferir()

        # 5. Mostrar Resultados
        self._mostrar_resultado_popup(conclusiones)

    def _mostrar_resultado_popup(self, conclusiones):
        # Ventana emergente personalizada
        popup = tk.Toplevel(self.root)
        popup.title("Informe Diagnóstico")
        popup.geometry("400x300")
        
        lbl_header = ttk.Label(popup, text="Resultados del Análisis", font=("Helvetica", 14, "bold"))
        lbl_header.pack(pady=15)

        # Área de texto para mostrar conclusiones
        text_area = tk.Text(popup, height=8, width=40, font=("Consolas", 10))
        text_area.pack(padx=20, pady=5)
        
        if not conclusiones:
             text_area.insert(tk.END, "No hay datos suficientes.")
        else:
            for c in conclusiones:
                text_area.insert(tk.END, f"• {c}\n\n")
        
        text_area.configure(state='disabled') # Hacer solo lectura

        btn_cerrar = ttk.Button(popup, text="Cerrar", command=popup.destroy)
        btn_cerrar.pack(pady=15)

# --- Ejecución ---
if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaExpertoGUI(root)
    root.mainloop()