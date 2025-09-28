import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import re

ALPHABET_DEFAULT = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

FREQUENCY = {
    "A": 8.2, "B": 1.5, "C": 2.8, "D": 4.3, "E": 13, "F": 2.2,
    "G": 2, "H": 6.1, "I": 7, "J": 0.15, "K": 0.77, "L": 4,
    "M": 2.4, "N": 6.7, "O": 7.5, "P": 1.9, "Q": 0.095, "R": 6,
    "S": 6.3, "T": 9.1, "U": 2.8, "V": 0.98, "W": 2.4, "X": 0.15,
    "Y": 2, "Z": 0.074
}

def vigenere(message, key, direction, alphabet):
    key_index = 0
    result = ""
    for char in message:
        if char not in alphabet:
            result += char
            continue
        msg_idx = alphabet.find(char)
        key_char = key[key_index % len(key)]
        key_idx = alphabet.find(key_char)
        if direction == "encrypt":
            new_idx = (msg_idx + key_idx) % len(alphabet)
        elif direction == "decrypt":
            new_idx = (msg_idx - key_idx) % len(alphabet)
        else:
            raise ValueError("Dirección inválida")
        result += alphabet[new_idx]
        key_index += 1
    return result

def kasiski(message, alphabet):
    message = re.sub(r'[^A-Z]', '', message.upper())
    if len(message) < 50:
        raise ValueError("El texto es demasiado corto para un análisis confiable.")
    
    sequences = find_repeats(message)
    if not sequences:
        raise ValueError("No se encontraron repeticiones suficientes.")
    
    key_length = find_key_length(sequences)
    key = find_key(message, key_length, alphabet)
    return key

def find_repeats(message):
    sequences = {}
    for seq_length in range(3, 6):
        for seq_begin in range(len(message) - seq_length):
            seq = message[seq_begin:seq_begin + seq_length]
            for i in range(seq_begin + seq_length, len(message) - seq_length):
                if message[i:i + seq_length] == seq:
                    if seq not in sequences:
                        sequences[seq] = []
                    sequences[seq].append(i - seq_begin)
    return sequences

def find_key_length(sequences):
    potential_accuracy = {}
    max_key_len = 20
    for i in range(2, max_key_len + 1):
        count = 0
        total = 0
        for dists in sequences.values():
            for dist in dists:
                total += 1
                if dist % i == 0:
                    count += 1
        if total > 0:
            potential_accuracy[i] = count / total
    potential_keys = [k for k, v in potential_accuracy.items() if v >= 0.6]
    if not potential_keys:
        raise ValueError("No se pudo estimar una longitud de clave confiable.")
    return max(potential_keys)

def find_key(message, key_length, alphabet):
    key = ""
    for pos in range(key_length):
        scored = {}
        for letter in alphabet:
            counts = {let: 0 for let in alphabet}
            idx = pos
            while idx < len(message):
                row = alphabet.find(message[idx])
                col = alphabet.find(letter)
                dec_char = alphabet[(row - col) % len(alphabet)]
                counts[dec_char] += 1
                idx += key_length
            score = sum(counts[char] * FREQUENCY[char] for char in alphabet)
            scored[letter] = score
        best_letter = max(scored, key=scored.get)
        key += best_letter
    return key

def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text_entry.delete("1.0", tk.END)
                text_entry.insert(tk.END, f.read())
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar el archivo: {e}")

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(result_text.get("1.0", tk.END).strip())
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar el archivo: {e}")

def process():
    mode = mode_var.get()
    text = text_entry.get("1.0", tk.END).strip()
    key = key_entry.get().strip().upper()
    normalize = normalize_var.get()
    alphabet = alphabet_entry.get().upper() or ALPHABET_DEFAULT

    if not text and mode != "analyze":
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "")
        return

    discarded = []
    if normalize == "strict":
        normalized_text = ""
        for c in text:
            c_upper = c.upper()
            if c_upper in alphabet:
                normalized_text += c_upper
            else:
                discarded.append(c)
        if discarded:
            messagebox.showinfo("Normalización", f"Caracteres descartados: {''.join(discarded)}")
        text = normalized_text
    else:  # lax
        normalized_text = text

    try:
        if mode in ["encrypt", "decrypt"]:
            if not key:
                raise ValueError("Clave requerida para cifrar/descifrar.")
            if len(key) == 0:
                raise ValueError("Clave vacía no permitida.")
            if not all(c in alphabet for c in key):
                raise ValueError("Clave contiene caracteres fuera del alfabeto.")
            result = vigenere(text, key, mode, alphabet)
        elif mode == "analyze":
            est_key = kasiski(text, alphabet)
            decrypted = vigenere(text, est_key, "decrypt", alphabet)
            result = f"Clave estimada: {est_key}\nTexto descifrado: {decrypted}"
        else:
            raise ValueError("Modo inválido.")
        
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, result)
    except ValueError as e:
        messagebox.showerror("Error", str(e))

# Configuración de la GUI
root = tk.Tk()
root.title("Cifrado Vigenère")

# Modo
mode_var = tk.StringVar(value="encrypt")
mode_label = ttk.Label(root, text="Modo:")
mode_label.grid(row=0, column=0, padx=5, pady=5)
mode_menu = ttk.OptionMenu(root, mode_var, "encrypt", "encrypt", "decrypt", "analyze")
mode_menu.grid(row=0, column=1, padx=5, pady=5)

# Texto
text_label = ttk.Label(root, text="Texto:")
text_label.grid(row=1, column=0, padx=5, pady=5)
text_entry = tk.Text(root, height=5, width=40)
text_entry.grid(row=1, column=1, padx=5, pady=5)

# Botón para cargar archivo
load_button = ttk.Button(root, text="Cargar archivo", command=load_file)
load_button.grid(row=1, column=2, padx=5, pady=5)

# Clave
key_label = ttk.Label(root, text="Clave:")
key_label.grid(row=2, column=0, padx=5, pady=5)
key_entry = ttk.Entry(root)
key_entry.grid(row=2, column=1, padx=5, pady=5)

# Normalización
normalize_var = tk.StringVar(value="lax")
normalize_label = ttk.Label(root, text="Normalización:")
normalize_label.grid(row=3, column=0, padx=5, pady=5)
normalize_menu = ttk.OptionMenu(root, normalize_var, "lax", "lax", "strict")
normalize_menu.grid(row=3, column=1, padx=5, pady=5)

# Alfabeto
alphabet_label = ttk.Label(root, text="Alfabeto (opcional):")
alphabet_label.grid(row=4, column=0, padx=5, pady=5)
alphabet_entry = ttk.Entry(root)
alphabet_entry.grid(row=4, column=1, padx=5, pady=5)

# Botón y Resultado
process_button = ttk.Button(root, text="Procesar", command=process)
process_button.grid(row=5, column=0, columnspan=2, pady=10)

result_label = ttk.Label(root, text="Resultado:")
result_label.grid(row=6, column=0, padx=5, pady=5)
result_text = tk.Text(root, height=5, width=40)
result_text.grid(row=6, column=1, padx=5, pady=5)

# Botón para guardar archivo
save_button = ttk.Button(root, text="Guardar resultado", command=save_file)
save_button.grid(row=6, column=2, padx=5, pady=5)

root.mainloop()