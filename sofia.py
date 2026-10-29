def main():
    print("Hola, soy Sofia.")
    print("Escribe 'salir' para terminar.")
 
    while True:
        mensaje = input("Tú: ")
        if mensaje.lower() == "salir":
            print("Sofia: Hasta luego.")
            break

        print(f"Sofia: Recibí tu mensaje: {mensaje}")
if __name__ == "__main__":
     main()
