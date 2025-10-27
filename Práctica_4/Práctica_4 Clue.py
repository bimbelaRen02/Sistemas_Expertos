import random
import time

# --- CONFIGURACIÓN BASE ---
sospechosos = ["Poseidón", "Hades", "Ares", "Atenea", "Hermes"]
armas = ["Rayo de Zeus", "Tridente de Poseidón", "Cetro del Inframundo", "Égida de Atenea", "Lanza de Ares"]
lugares = ["Monte Olimpo", "Inframundo", "Océanos", "Templo de Atenea", "Odeón de Herodes Ático"]

# --- ELECCIÓN SECRETA ---
culpable = random.choice(sospechosos)
arma_asesina = random.choice(armas)
lugar_crimen = random.choice(lugares)

# --- ELECCIÓN DE 3 COSAS QUE NO SON ---
no_sospechoso = random.choice([s for s in sospechosos if s != culpable])
no_arma = random.choice([a for a in armas if a != arma_asesina])
no_lugar = random.choice([l for l in lugares if l != lugar_crimen])

# --- INTRODUCCIÓN ---
def narrar(texto):
    for c in texto:
        print(c, end='', flush=True)
        time.sleep(0.015)
    print()

narrar("⚡ BIENVENIDO, MORTAL ⚡")
narrar("El trono del Olimpo yace vacío. Zeus ha muerto, y el cielo retumba de sospecha...")
narrar("Tu misión como oráculo es descubrir quién lo asesinó, con qué arma divina y en qué lugar sagrado.\n")

# --- REVELACIONES INICIALES ---
narrar("Los vientos del destino te revelan tres verdades iniciales:")
narrar(f"❌ {no_sospechoso} es inocente.")
narrar(f"❌ El arma '{no_arma}' no fue utilizada.")
narrar(f"❌ En '{no_lugar}' no ocurrió el crimen.\n")

# --- VARIABLES DE CONTROL ---
intentos = 0
max_intentos = 8
juego_activo = True

# --- MENÚ PRINCIPAL ---
def menu_principal():
    print("\n¿Qué deseas hacer?")
    print("1. Preguntar al oráculo 🔮")
    print("2. Ya sé qué sucedió ⚡")
    opcion = input("> ")
    return opcion.strip()

# --- PREGUNTA ---
def realizar_pregunta():
    global intentos
    print("\n¿Quién crees que lo hizo?")
    for i, s in enumerate(sospechosos, start=1):
        print(f"{i}. {s}")
    sospechoso = sospechosos[int(input("> ")) - 1]

    print("\n¿Qué arma crees que usó?")
    for i, a in enumerate(armas, start=1):
        print(f"{i}. {a}")
    arma = armas[int(input("> ")) - 1]

    print("\n¿Dónde crees que sucedió?")
    for i, l in enumerate(lugares, start=1):
        print(f"{i}. {l}")
    lugar = lugares[int(input("> ")) - 1]

    intentos += 1
    print(f"\n🌩️ Pregunta #{intentos}:")

    # Revisión en orden: sospechoso, arma, lugar
    if sospechoso != culpable:
        narrar(f"{sospechoso} no ha sido el asesino. Jura por el río Estigia su inocencia.")
    elif arma != arma_asesina:
        narrar(f"El arma '{arma}' no muestra el poder que arrebató la vida del dios del trueno.")
    elif lugar != lugar_crimen:
        narrar(f"En '{lugar}' los ecos del crimen no resuenan. Ahí no ocurrió nada.")
    else:
        narrar("🌩️ ¡El oráculo guarda silencio! Eso solo significa una cosa...")
        narrar("Todas tus suposiciones son ciertas.")
        resolver(True)
        return

    if intentos >= max_intentos:
        narrar("\n☠️ Has agotado tus preguntas. Los dioses exigen una respuesta final...")
        resolver(False)

# --- RESOLUCIÓN ---
def resolver(victoria_directa):
    global juego_activo
    print("\n--- ⚖️ JUICIO FINAL ⚖️ ---")
    print("Declara tu veredicto ante los dioses:")

    print("\n¿Quién fue el asesino?")
    for i, s in enumerate(sospechosos, start=1):
        print(f"{i}. {s}")
    sospechoso_final = sospechosos[int(input("> ")) - 1]

    print("\n¿Qué arma utilizó?")
    for i, a in enumerate(armas, start=1):
        print(f"{i}. {a}")
    arma_final = armas[int(input("> ")) - 1]

    print("\n¿Dónde ocurrió el crimen?")
    for i, l in enumerate(lugares, start=1):
        print(f"{i}. {l}")
    lugar_final = lugares[int(input("> ")) - 1]

    if (sospechoso_final == culpable and
        arma_final == arma_asesina and
        lugar_final == lugar_crimen):
        narrar("\n🏆 ¡Has revelado la verdad! El Olimpo se inclina ante tu sabiduría.")
        narrar(f"El asesino fue {culpable}, con el {arma_asesina}, en el {lugar_crimen}.")
        narrar("Te has ganado el trono del mismísimo Zeus ⚡")
    else:
        narrar("\n🔥 Has fallado. Los dioses te condenan al Tártaro.")
        narrar(f"La verdad era: {culpable} lo asesinó con el {arma_asesina} en el {lugar_crimen}.")
    juego_activo = False

# --- BUCLE PRINCIPAL ---
while juego_activo:
    opcion = menu_principal()
    if opcion == "1":
        realizar_pregunta()
    elif opcion == "2":
        resolver(False)
    else:
        print("Opción no válida. Intenta nuevamente.")