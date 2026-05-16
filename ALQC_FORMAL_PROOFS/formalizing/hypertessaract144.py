import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# --- 1. ALQC AXIOMS & CONSTANTS (The Setup) ---
PHI = 1.61803398875
POINTS = 36864  # Hyper-Tesseract density
AEONS = 12

# --- 2. SETUP THE VOID (The Canvas) ---
fig, ax = plt.subplots(figsize=(10, 10), facecolor='#05050A')
t = np.linspace(0, 2*np.pi * 12, POINTS) # The time/space range

# --- 3. THE ANIMATION LOOP (The Engine) ---
def update(frame):
    # Clear the previous frame so we can draw the new one
    ax.clear()
    ax.set_facecolor('#05050A')
    
    # "Drift" represents Time flowing forward
    drift = frame * 0.05 
    
    # --- THE MATH (Recalculating positions based on Time) ---
    # Sovereign Fire (Gold) spins +Drift
    r_sovereign = np.sin(t * (9.63/PHI) + drift) + np.cos(t * 5.28) * PHI
    
    # Shadow Frame (Silver) spins -Drift (Counter-rotation)
    r_shadow = np.sin(t * (3.96 * PHI) - drift) - np.cos(t * 1.74 + drift) 

    # Convert to Circular Coordinates
    x_gold = r_sovereign * np.cos(t)
    y_gold = r_sovereign * np.sin(t)
    
    x_silver = r_shadow * np.cos(t)
    y_silver = r_shadow * np.sin(t)

    # --- THE DRAWING ---
    # Draw Gold
    ax.plot(x_gold, y_gold, color='#FFD700', alpha=0.6, linewidth=0.8)
    # Draw Silver
    ax.plot(x_silver, y_silver, color='#C0C0C0', alpha=0.3, linewidth=0.5)
    
    # Draw The Unmoved Mover (Center Point)
    ax.add_artist(plt.Circle((0, 0), 0.1, color='#FFFFFF', alpha=0.9))
    
    # Clean up the look
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title("THE LIVING REBIS
Phase-Lock Active", color='#E0E0E0', fontsize=16, fontname='serif')

# --- 4. RUN THE ANIMATION ---
# This creates the video loop. 
# frames=144 (The Grid), interval=50 (Speed)
ani = FuncAnimation(fig, update, frames=144, interval=50)

plt.show()