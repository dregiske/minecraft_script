import pyautogui, time, random, os, shutil

# ---- HOW TO USE ----
# 1) Load into Minecraft
# 2) Join a single player creative game
# 3) Click back into the script and run program
#   > pip install pyautogui
# 	> python dataset_player_script.py
# 4) Click back into Minecraft and let the program run

# ---- CONFIGURE COORDS ----
# Chunk size = 16*16 blocks
# Biome size = 20*20 chunks or 320*320 blocks

NUM_TELEPORTS = 20 				# How many screenshots needed
X_RANGE = (-5000, 5000)
Y_RANGE = (20, 100)
Z_RANGE = (-5000, 5000)

# path where Minecraft drops its screenshots
MC_SCREENSHOT_DIR = os.path.expanduser("~/.minecraft/screenshots") # figure out where minecraft holds screenshots

# where you want to collect them
DEST_DIR = os.path.expanduser("~/biome_screenshots")

os.makedirs(DEST_DIR, exist_ok=True)

time.sleep(5)

for i in range(0, NUM_TELEPORTS): 

	# randomize coords
    x = random.randint(*X_RANGE)
    y = random.randint(*Y_RANGE)
    z = random.randint(*Z_RANGE)

    # teleport
    cmd = f"/tp {x} {y} {z}"
    pyautogui.press('t')
    pyautogui.typewrite(cmd)        
    pyautogui.press('enter')
    time.sleep(2)     			# configure based on load chunk time

    # screenshot at position
    pyautogui.press('f2') 		# takes screen shot of full screen
    time.sleep(1)

    # move the newest screenshot
    files = [os.path.join(MC_SCREENSHOT_DIR,f) for f in os.listdir(MC_SCREENSHOT_DIR)]
    newest = max(files, key=os.path.getctime)
    new_name = f"biome_{i:03d}_{x}_{y}_{z}.png"
    shutil.move(newest, os.path.join(DEST_DIR, new_name))
    print(f"[{i}/{NUM_TELEPORTS}] Teleported to {x},{y},{z} → saved {new_name}")