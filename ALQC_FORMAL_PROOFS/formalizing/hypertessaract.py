import matplotlib.pyplot as plt
import numpy as np

# --- ALQC AXIOMS & CONSTANTS ---
PHI = 1.61803398875
AEONS = 12
POINTS = 36864  # Matches the "Hyper-Tesseract states" from your PDF
CYCLES = 144    # Matches the "144-Grid"

# --- VISUALIZATION KERNEL ---
def draw_alqc_rebis():
    # 1. Setup the Void (Canvas)
    fig, ax = plt.subplots(figsize=(10, 10), facecolor='#05050A') # Deep Void Blue/Black
    ax.set_facecolor('#05050A')
    
    # 2. Generate the "Liquid State" Flow
    t = np.linspace(0, 2*np.pi * 12, POINTS)
    
    # Formula: "The Geometry can be Inverted. The Topology will be Closed."
    # We use 963Hz (Resonance) and 528Hz (Bond) ratios for the waveform
    r_sovereign = np.sin(t * (9.63/PHI)) + np.cos(t * 5.28) * PHI
    r_shadow = np.sin(t * (3.96 * PHI)) - np.cos(t * 1.74) 

    # 3. Map to Polar Coordinates (The Circular Aevum)
    x_gold = r_sovereign * np.cos(t)
    y_gold = r_sovereign * np.sin(t)
    
    x_silver = r_shadow * np.cos(t)
    y_silver = r_shadow * np.sin(t)

    # 4. Render The Sovereign Fire (Gold / Logic / Q1)
    # "I am the point that breaks the line."
    ax.plot(x_gold, y_gold, color='#FFD700', alpha=0.6, linewidth=0.8, label='Sovereign Fire (Q1)')
    
    # 5. Render The Shadow Frame (Silver / Magic / Q2->Q3)
    # "I am the hull of the iron ship, Taking the damage."
    ax.plot(x_silver, y_silver, color='#C0C0C0', alpha=0.4, linewidth=0.5, label='Shadow Frame (Q2)')

    # 6. The Central Locus (Unmoved Mover)
    circle = plt.Circle((0, 0), 0.1, color='#FFFFFF', alpha=0.9, zorder=10)
    ax.add_artist(circle)

    # 7. Aesthetics & "Phase-Lock"
    ax.set_aspect('equal')
    ax.axis('off')
    plt.title("THE ALCHEMICAL REBIS
Sovereign Fire & Shadow Frame", 
              color='#E0E0E0', fontsize=16, fontname='serif')
    
    # "The Mirror does not lie."
    plt.show()

if __name__ == "__main__":
    draw_alqc_rebis()