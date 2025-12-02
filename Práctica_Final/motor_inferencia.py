import json

class MotorInferencia:

    def __init__(self, ruta_json):
        with open(ruta_json, "r", encoding="utf-8") as f:
            self.data = json.load(f)

        self.rules = self.data["rules"]
        self.facts = set()  # hechos que el usuario confirma

    def agregar_hecho(self, hecho):
        """Agrega hechos al sistema (respuestas del usuario)"""
        self.facts.add(hecho)

    def evaluar_regla(self, regla):
        """Verifica si una regla se cumple"""
        condiciones = regla["if"]
        return all(cond in self.facts for cond in condiciones)

    def inferir(self):
        """Evalúa todas las reglas para obtener una conclusión"""
        conclusiones = []

        for regla in self.rules:
            if self.evaluar_regla(regla):
                conclusiones.append(regla["then"])

        # Si ninguna regla aplica:
        if not conclusiones:
            return ["No se encontró diagnóstico claro. Considere diagnósticos diferenciales."]

        return conclusiones