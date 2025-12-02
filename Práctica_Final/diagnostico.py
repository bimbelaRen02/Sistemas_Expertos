from motor_inferencia import MotorInferencia

# Mapeo actualizado
MAPEO_HECHOS = {
    1: "fiebre_alta",
    2: "tos",
    3: "coriza",
    4: "conjuntivitis",
    5: "koplik",
    6: "exantema",
    7: "contacto_sospechoso",
    8: "vacunado",
    # --- Nuevos mapeos ---
    9: "fiebre_baja",
    10: "adenopatia_retroauricular",
    11: "fiebre_alta_desaparece",
    12: "exantema_posterior",
    13: "faringitis",
    14: "exantema_tipo_lija"
}

def preguntar_usuario(preguntas):
    hechos_confirmados = []

    print("\n--- Encuesta médica ---\n")

    for p in preguntas:
        while True:
            respuesta = input(f"{p['text']} (s/n): ").lower()
            if respuesta in ["s", "n"]:
                break
            print("Respuesta inválida. Use s/n.")

        if respuesta == "s":
            hechos_confirmados.append(MAPEO_HECHOS[p["id"]])

    return hechos_confirmados


def main():
    sistema = MotorInferencia("sarampion_db.json")

    preguntas = sistema.data["questions"]
    hechos = preguntar_usuario(preguntas)

    for h in hechos:
        sistema.agregar_hecho(h)

    # Normalizar la condición obligatoria (OR lógico entre tos/coriza/conjuntivitis)
    if any(h in sistema.facts for h in ["tos", "coriza", "conjuntivitis"]):
        sistema.agregar_hecho("tos_o_coriza_o_conjuntivitis")

    conclusiones = sistema.inferir()

    print("\n--- Resultados ---")
    for c in conclusiones:
        print("•", c)


if __name__ == "__main__":
    main()