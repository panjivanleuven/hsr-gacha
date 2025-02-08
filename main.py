import tkinter as tk
import random
import asyncio

BASE_RATE_5_STAR = 0.6
PITY_THRESHOLD = 90
GUARANTEED_RATE_ON = 100

RATE_ON_CHARACTERS = ["Aglaea"]
RATE_OFF_CHARACTERS = ["Himeko", "Welt", "Bronya", "Bailu", "Gepard", "Yanqing", "Clara"]

attempts = 0
pity_counter = 0
inventory = []

async def perform_gacha():
    global attempts, pity_counter, inventory

    attempts += 1
    pity_counter += 1

    await asyncio.sleep(0.5)

    if pity_counter >= PITY_THRESHOLD:
        is_5_star = True
    else:
        is_5_star = random.random() < (BASE_RATE_5_STAR / 100)

    if is_5_star:
        pity_counter = 0
        if random.random() < 0.5:
            character = random.choice(RATE_ON_CHARACTERS)
            result = f"RATE-ON - {character}"
        else:
            character = random.choice(RATE_OFF_CHARACTERS)
            result = f"RATE-OFF - {character}"

        inventory.append(character)
        return result
    else:
        return "Bintang 4 atau lebih rendah"

async def handle_single_gacha():
    result = await perform_gacha()
    update_gui(result)

async def handle_multi_gacha():
    results = []
    for _ in range(10):
        result = await perform_gacha()
        results.append(result)
    update_gui("\n".join(results))

def update_gui(result):
    result_label.config(text=f"Percobaan Terakhir:\n{result}")

    inventory_text = "\n".join(inventory)
    inventory_label.config(text=f"Inventory:\n{inventory_text}")
    print(f"Pity: {pity_counter}")

def run_asyncio(coroutine):
    asyncio.run(coroutine)

print("Memulai Tkinter...")
window = tk.Tk()
window.title("Gacha Honkai: Star Rail")
window.geometry("600x600")

title_label = tk.Label(window, text="Gacha Honkai: Star Rail Simulator, Lite", font=("Arial", 14))
title_label.pack(pady=20)

gacha_button = tk.Button(window, text="Gacha 1x", command=lambda: run_asyncio(handle_single_gacha()), bg="blue", fg="white", font=("Arial", 12))
gacha_button.pack(pady=10)

multi_gacha_button = tk.Button(window, text="Gacha 10x", command=lambda: run_asyncio(handle_multi_gacha()), bg="green", fg="white", font=("Arial", 12))
multi_gacha_button.pack(pady=10)

result_label = tk.Label(window, text="Hasil gacha akan muncul di sini.", font=("Arial", 12), wraplength=380)
result_label.pack(pady=20)

inventory_label = tk.Label(window, text="Inventory:\n", font=("Arial", 12), justify="left")
inventory_label.pack(pady=20)

window.mainloop()
