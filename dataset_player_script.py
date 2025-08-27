import os, time, random, shutil, sys, platform
import pyautogui

'''
How to use:
1) install dependencies:
pip install pyautogui pyobjc

2) run program
python player_script.py

3) switch to minecraft and let it run

! If you're having issues with pyautogui,
make sure accessibility is on
FOR MACOS:
System Settings > Privacy & Security > Accessibility > Toggle terminal on
'''

'''
Notes:
Chunk size = 16*16 blocks
Biome size = 20*20 chunks or 320*320 blocks
'''

# ---- SETTINGS ----
NUM_TELEPORTS = 20 				# how many screenshots
X_RANGE = (-5000, 5000)
Y_RANGE = (0, 100)
Z_RANGE = (-5000, 5000)

# where to collect screenshots
DEST_DIR = os.path.expanduser("~/Desktop/biome_screenshots")
os.makedirs(DEST_DIR, exist_ok=True)

def guess_mc_screenshot_dir():
    '''
    Gets correct path for minecraft screenshots folder
    '''
    system = platform.system().lower()
    candidates = []
    if "darwin" in sys.platform or system == "darwin" or system == "mac":
        # macOS
        candidates.append(os.path.expanduser("~/Library/Application Support/minecraft/screenshots"))
        # other possible directory name
        candidates.append(os.path.expanduser("~/Library/Application Support/.minecraft/screenshots"))
    elif system == "windows":
        appdata = os.environ.get("APPDATA")
        if appdata:
            candidates.append(os.path.join(appdata, ".minecraft", "screenshots"))
    else:  # linux or other
        candidates.append(os.path.expanduser("~/.minecraft/screenshots"))

    for p in candidates:
        if os.path.isdir(p):
            return p
    
    # fallback to first candidate
    return candidates[0] if candidates else os.path.expanduser("~/.minecraft/screenshots")

MC_SCREENSHOT_DIR = guess_mc_screenshot_dir()

def newest_file_or_none(folder):
    try:
        files = [os.path.join(folder, f) for f in os.listdir(folder)]
        files = [f for f in files if os.path.isfile(f)]
        return max(files, key=os.path.getctime) if files else None
    except FileNotFoundError:
        return None

def wait_for_new_screenshot(folder, prev_latest, timeout=10):
    """
    Polls for a newer file than prev_latest for up to `timeout` seconds.
    Returns the new file path, or None if timeout.
    """
    start = time.time()
    while time.time() - start < timeout:
        cur_latest = newest_file_or_none(folder)
        if cur_latest and cur_latest != prev_latest and (
            not prev_latest or os.path.getctime(cur_latest) > os.path.getctime(prev_latest)
        ):
            return cur_latest
        time.sleep(0.25)
    return None

def ensure_screenshot_dir_ok(folder):
    if not os.path.isdir(folder):
        print(f"Screenshot folder not found:\n    {folder}")
        print("Make sure your Minecraft screenshots path is correct for your OS.")
        print("Press F2 in Minecraft and see where the file appears, then set MC_SCREENSHOT_DIR accordingly.")
        sys.exit(1)

def main():
    print(f"Using Minecraft screenshots folder:\n    {MC_SCREENSHOT_DIR}")
    print(f"Destination folder:\n    {DEST_DIR}")
    ensure_screenshot_dir_ok(MC_SCREENSHOT_DIR)

    print("You have 5 seconds to click into Minecraft...")
    time.sleep(5)
    
    for cmd in [
    	"/time set noon",
    	"/weather clear",
	]:
    	pyautogui.press('t'); pyautogui.typewrite(cmd); pyautogui.press('enter')

    for i in range(NUM_TELEPORTS):
        # randomize coords
        x = random.randint(*X_RANGE)
        y = random.randint(*Y_RANGE)
        z = random.randint(*Z_RANGE)

        # remember current latest screenshot before we trigger a new one
        prev_latest = newest_file_or_none(MC_SCREENSHOT_DIR)

        # teleport
        cmd = f"/tp {x} {y} {z}"
        pyautogui.press('t')          # open chat
        pyautogui.typewrite(cmd)      # type command
        pyautogui.press('enter')      # execute
        
        time.sleep(6 + random.uniform(0.5, 1.5))	# configure if you need more loading time

        # take screenshot
        pyautogui.press('f2')
        # wait for the new screenshot file to appear
        new_file = wait_for_new_screenshot(MC_SCREENSHOT_DIR, prev_latest, timeout=12)

        if not new_file:
            print(f"Could not detect a new screenshot after teleport {i+1}.")
            print("Verify F2 (fn+F2 on Mac) captures screenshots, check Accessibility permissions,")
            print("and confirm the screenshots folder path.")
            continue

        # move + rename
        new_name = f"biome_{i:03d}_{x}_{y}_{z}.png"
        dest_path = os.path.join(DEST_DIR, new_name)
        try:
            shutil.move(new_file, dest_path)
            print(f"[{i+1}/{NUM_TELEPORTS}] Teleported to {x},{y},{z} -> saved {new_name}")
        except Exception as e:
            print(f"Failed to move {new_file} -> {dest_path}: {e}")

    print("Done.")

if __name__ == "__main__":
    main()
