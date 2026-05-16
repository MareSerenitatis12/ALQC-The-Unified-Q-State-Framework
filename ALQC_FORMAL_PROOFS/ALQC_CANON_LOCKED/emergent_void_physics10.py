#!/usr/bin/env python3
"""
ALQC INTEGRATED: Emergent Void Physics + FETU Ground + S6 Bridge
===========================================================================

FULL SYSTEM INTEGRATION:
1. FETU (7.83 Hz): 'â£' Spiral Anchor. Rotates on independent axis (Angle * PHI).
2. S6 Bridge (210.42 Hz): Invisible "Air" Honeycomb. Tunneling Logic via PHI tolerance.
3. Optimization: Pre-rendered Glyph Cache for high-speed phase entanglement.
4. 4D Freedom: Z/W axes unlocked.
5. ALQC Core: Emergent Entropy & Rotation Memory.

"""

import pygame
import sys
import os
import math
import numpy as np

# --- 1. ALQC CORE CONSTANTS (DEFINED FIRST) ---
PHI = 1.61803398875
WIDTH, HEIGHT = 1000, 1000
BACKGROUND_COLOR = (5, 5, 10)

# --- 2. ENTROPY & FIELD CLASSES ---

class ALQCFieldEntropy:
    """Pure ALQC stochasticity. No external seed. Self-referential phase."""
    def __init__(self, seed_phase=0.0):
        self.phase_state = seed_phase
        self.entropy_accumulator = 0.0
        self.aeon_phase_offsets = {}

    def _aeon_phase_shift(self, aeon_key):
        if aeon_key not in self.aeon_phase_offsets:
            base_phase = (self.phase_state * PHI) % 1.0
            self.aeon_phase_offsets[aeon_key] = base_phase
        return self.aeon_phase_offsets[aeon_key]

    def field_rand(self):
        """The â© Entropic Source."""
        self.phase_state = (self.phase_state * 1.4142135623730951 + PHI) % 1.0
        self.entropy_accumulator = (self.entropy_accumulator + self.phase_state) % 1.0
        return (self.phase_state + self.entropy_accumulator) % 1.0

    def field_rand_gauss(self, mu, sigma):
        samples = 12
        sum_phases = sum(self.field_rand() for _ in range(samples))
        normalized = (sum_phases - 6.0)
        return mu + sigma * normalized

    def field_rand_uniform(self, a, b):
        return a + (b - a) * self.field_rand()

    def field_rand_int(self, min_val, max_val):
        return min_val + int(self.field_rand() * (max_val - min_val + 1))

    def field_rand_choice(self, seq):
        return seq[self.field_rand_int(0, len(seq) - 1)]

class FETU_GroundState:
    """
    The Anchor of the Void (7.83 Hz).
    Shape: 'â£' (Spiral/Comma).
    Function: Phase-Locks 7.83Hz particles to the geometric center.
    Rotation: Rotates on a Shifted Axis (Angle * PHI) to avoid overlap.
    """
    def __init__(self, field_entropy):
        self.F = field_entropy
        self.points = []
        self._generate_attractor_shape()
        
    def _generate_attractor_shape(self):
        # Normalized coordinates centered at 0,0
        num_points = 120
        for i in range(num_points):
            t = i / 12.0  # Angle step
            r = 0.05 * math.exp(0.14 * t)
            x = r * math.cos(t)
            y = r * math.sin(t) - 0.2 
            self.points.append((x, y))
            
    def apply_phase_lock(self, e, global_angle):
        freq = abs(e['aeon']['freq'])
        delta_f = abs(freq - 7.83)
        
        # RESONANCE CHECK (Tolerance = PHI)
        if delta_f < PHI:
            idx = int((e['x'] * 50 + e['y'] * 50) % len(self.points))
            raw_tx, raw_ty = self.points[idx]
            
            # INDEPENDENT ROTATION (Polyrhythmic Axis)
            theta = global_angle * PHI
            cos_t = math.cos(theta)
            sin_t = math.sin(theta)
            
            target_x = raw_tx * cos_t - raw_ty * sin_t
            target_y = raw_tx * sin_t + raw_ty * cos_t
            
            strength = (1.0 - (delta_f / PHI)) * 0.02
            e['dx'] += (target_x - e['x']) * strength
            e['dy'] += (target_y - e['y']) * strength
            
            if delta_f < 0.1:
                e['stress'] += 0.5 

class SOR_BridgeCourt:
    """
    The S6 Manifestation Coupling (Court of SOR).
    Frequency: 210.42 Hz (Purity/Space).
    Op-Code: BRIDGE (Teleportation/Dimensional Swap).
    """
    def __init__(self, field_entropy):
        self.F = field_entropy
        self.hex_radius = 0.4
        # Derived from Phi Harmonics
        self.phi_tolerance = 1.0 / (PHI ** 3)
        
    def _get_hex_purity(self, x, y):
        q = (2./3 * x) / self.hex_radius
        r = (-1./3 * x + math.sqrt(3)/3 * y) / self.hex_radius
        rx, ry, rz = round(q), round(r), round(-q-r)
        dx, dy, dz = abs(rx-q), abs(ry-r), abs(rz-(-q-r))
        if dx > dy and dx > dz: rx = -ry-rz
        elif dy > dz: ry = -rx-rz
        else: rz = -rx-ry
        cx = self.hex_radius * (3./2 * rx)
        cy = self.hex_radius * (math.sqrt(3)/2 * rx + math.sqrt(3) * ry)
        dist = math.sqrt((x - cx)**2 + (y - cy)**2)
        purity = max(0, 1.0 - (dist / (self.hex_radius * 0.8)))
        return purity

    def apply_bridge_operator(self, e):
        """Checks for Tunneling Event (Invisible Wall Interaction)"""
        purity = self._get_hex_purity(e['x'], e['y'])
        
        if purity < self.phi_tolerance:
            bridge_chance = 0.05 + (e.get('stress', 0) * 0.2)
            if self.F.field_rand() < bridge_chance:
                # EXECUTE BRIDGE (Dimensional Swap)
                temp_dx = e['dx']
                temp_dy = e['dy']
                e['dx'] = e['dw'] * -1.0 
                e['dy'] = e['dz'] * -1.0
                e['dw'] = temp_dx
                e['dz'] = temp_dy
                e['z'] += 0.5  # Visual Pop
                return True
        return False

class ALQCRotationMemory:
    """The M.A.S. Chain Operator."""
    def __init__(self, field_entropy):
        self.F = field_entropy
        self.phase_memory = {}

    def emergent_cos_sin(self, angle_key, x, y, stress=0.0):
        region_key = f"{int(x/50)}_{int(y/50)}_{angle_key}"
        if region_key not in self.phase_memory:
            self.phase_memory[region_key] = {
                "phase": self.F.field_rand(),
                "drift": abs(self.F.field_rand_gauss(0.004, 0.002))
            }
        mem = self.phase_memory[region_key]
        debt_factor = stress * (1.0 + self.F.field_rand_gauss(0.0, 0.12))
        mem["phase"] += mem["drift"] * (1.0 + debt_factor)
        t = mem["phase"] % 1.0
        cos_e = 4.0 * abs(t - 0.5) - 1.0
        sin_e = 4.0 * abs((t + 0.25) % 1.0 - 0.5) - 1.0
        return cos_e, sin_e

    def emergent_distance(self, dx, dy, dz=0.0, dw=0.0):
        accumulated = abs(dx) + abs(dy) + abs(dz) + abs(dw)
        if accumulated == 0.0: return 0.0
        relationship_factor = 1.0 + self.F.field_rand_gauss(0.0, 0.08)
        return accumulated * relationship_factor / 2.0

# --- 3. GLOBAL INITIALIZATION ---
alqc_entropy = ALQCFieldEntropy()
alqc_ops = ALQCRotationMemory(alqc_entropy)
sor_bridge = SOR_BridgeCourt(alqc_entropy)
fetu_ground = FETU_GroundState(alqc_entropy)

# --- 4. CONFIGURATION & CONSTANTS ---
PARTICLE_COUNT = 5000
SIGH_STRESS_BALL_COUNT = 4

ESCAPE_LIMIT = 5.0
MIN_COHERENCE_RADIUS = 0.6
MAX_COHERENCE_RADIUS = 1.2
COHERENCE_REDUCTION_STRENGTH = 0.85
MAX_KINETIC_STRESS = 300.0

# Reflected/Boundary constants
BOUNDARY_MEM_RES = 160
BOUNDARY_MEM_DECAY = 0.992
BOUNDARY_MEM_DEPOSIT = 0.085
BOUNDARY_MEM_SAMPLE_GAIN = 0.006
BOUNDARY_SHELL_INNER = 0.88
BOUNDARY_SHELL_OUTER = 1.02
BOUNDARY_MEM_MAX = 2.5

REFLECT_RING_RADIUS = 0.92
REFLECT_RING_WIDTH = 0.06
REFLECT_CHARGE_GAIN = 0.18
REFLECT_CHARGE_DECAY = 0.975
REFLECT_DELAY_FRAMES = 48
REFLECT_FORCE_GAIN = 0.00075
REFLECT_STRESS_ROUTE = 0.12

L_RB_MAX_RATE = 0.015
ELVEN_RESPONSE_GAIN = 0.0005
NODE_CHARGE_DAMP = 0.992
BASE_GLYPH_ALPHA = 4
SHADOW_LOCUS_COLOR = (255, 0, 50)
KLEIN_COLOR = (15, 15, 25)

# 5e Identity Seam
IDENTITY_EPS = 1e-12
MICRO_SCALE = 0.085
A10_RESONANCE = 963.0
A3_GATE = 528.00
BINDING_RATIO = A10_RESONANCE / A3_GATE
SEAM_CHARGE_DECAY = 0.992
SEAM_CHARGE_RATE = 0.008
SEAM_RELEASE_THRESHOLD = 0.7
SEAM_RELEASE_GAIN = 0.15
E_BIND_STRENGTH = 0.03

# Void Anchors
VOID_ANCHOR_RADIUS_PX = 120.0
VOID_ANCHOR_STRENGTH = 0.0003
VOID_ANCHOR_DAMP_MAX = 0.025
VOID_CORNER_POLARITY = [+1, -1, +1, -1]
SHADOW_LOCUS_POSITIONS = [
    (50, 50), (WIDTH - 50, 50), 
    (WIDTH - 50, HEIGHT - 50), (50, HEIGHT - 50)
]

# Primary Aeons
PRIMARY_AEONS_GLYPHS = [
    {"glyph": ".", "freq": 7.83, "color": (155, 89, 182)},
    {"glyph": ".", "freq": 174.0, "color": (52, 152, 219)},
    {"glyph": ".", "freq": 528.00, "color": (231, 76, 60)},
    {"glyph": ".", "freq": 432.00, "color": (255, 90, 70)},
    {"glyph": ".", "freq": 741.0, "color": (60, 180, 255)},
    {"glyph": ".", "freq": 210.42, "color": (120, 70, 150)},
    {"glyph": ".", "freq": 126.22, "color": (200, 120, 220)},
    {"glyph": ".", "freq": 852.0, "color": (40, 120, 180)},
    {"glyph": ".", "freq": 285.00,  "color": (200, 60, 50)},
    {"glyph": ".", "freq": 963.00, "color": (140, 80, 160)},
    {"glyph": ".", "freq": 396.0, "color": (52, 152, 219)},
    {"glyph": ".", "freq": 639.0, "color": (180, 100, 200)},
]
LESSER_AEON_COUNT = 12
LESSER_GLYPH_SYMBOL = '.'
LESSER_AEON_COLOR = (100, 100, 100)

# --- 5. HELPER FUNCTIONS ---

def _identity_seam_apply(e, R0):
    x, y, z, w = e.get('x', 0.0), e.get('y', 0.0), e.get('z', 0.0), e.get('w', 0.0)
    r2 = x*x + y*y + z*z + w*w
    inv = (R0 * R0) / (r2 + IDENTITY_EPS) * BINDING_RATIO
    
    tx = -x * inv * MICRO_SCALE
    ty = -y * inv * MICRO_SCALE
    tz = -z * inv * MICRO_SCALE
    tw = -w * inv * MICRO_SCALE
    
    c = e.get('seam_charge', 0.0)
    displacement = abs(tx - x) + abs(ty - y) + abs(tz - z) + abs(tw - w)
    c = c * SEAM_CHARGE_DECAY + displacement * SEAM_CHARGE_RATE
    
    if c > SEAM_RELEASE_THRESHOLD:
        excess = c - SEAM_RELEASE_THRESHOLD
        e['stress'] = max(0.0, e.get('stress', 0.0) + excess * SEAM_RELEASE_GAIN)
        c = SEAM_RELEASE_THRESHOLD * 0.65
    
    e['seam_charge'] = c
    if 'dx' in e:
        e['dx'] += (tx - x) * E_BIND_STRENGTH
        e['dy'] += (ty - y) * E_BIND_STRENGTH
        e['dz'] += (tz - z) * E_BIND_STRENGTH
        e['dw'] += (tw - w) * E_BIND_STRENGTH

def _get_triquatra_points(center_x, center_y, angle):
    base_radius = 40
    num_lobes = 3
    lobe_points = []
    for i in range(num_lobes):
        t = angle + (i * 2 * math.pi / num_lobes)
        x = center_x + base_radius * math.cos(t) * 1.5
        y = center_y + base_radius * math.sin(t) * 1.5
        lobe_points.append((x, y))
    return lobe_points

class ShadowLocus:
    def __init__(self, chronos_lock, position):
        self.lock = chronos_lock
        self.position = position
        self.angle = 0.0
        self.current_stress = 0.0
        self.entities = [self._create_entity_logic(i) for i in range(12)]

    def _create_entity_logic(self, i):
        e = {}
        e['aeon'] = PRIMARY_AEONS_GLYPHS[i]
        e['base_surface'] = self.lock.font.render(e['aeon']['glyph'], True, SHADOW_LOCUS_COLOR)
        t = i * 2 * math.pi / 12
        e['x_offset'] = 15 * math.cos(t)
        e['y_offset'] = 15 * math.sin(t)
        
        norm_x = (self.position[0] - WIDTH/2) / (WIDTH/2)
        norm_y = (self.position[1] - HEIGHT/2) / (HEIGHT/2)
        e['x'] = norm_x + e['x_offset'] / (WIDTH/2)
        e['y'] = norm_y + e['y_offset'] / (HEIGHT/2)
        e['z'], e['w'] = 0.0, 0.0
        e['dx'], e['dy'], e['dz'], e['dw'] = 0.0, 0.0, 0.0, 0.0
        e['stress'] = 0.0
        e['seam_charge'] = 0.0
        e['reflect_charge'] = 0.0
        e['reflect_age'] = 0
        return e

    def _calculate_inverse_stress(self, primary_stress):
        normalized_primary_stress = math.tanh(primary_stress / MAX_KINETIC_STRESS)
        inverse_stress = (1.0 - normalized_primary_stress) * (MAX_KINETIC_STRESS / 4.0)
        return inverse_stress

    def run_projection(self):
        primary_stress = self.lock.primary_kinetic_stress
        self.current_stress = self._calculate_inverse_stress(primary_stress)
        self.angle += 0.05
        
        for e in self.entities:
            R_sq = e['x']**2 + e['y']**2 + e['z']**2 + e['w']**2
            R = math.sqrt(R_sq)
            if R < -0.000000001: _identity_seam_apply(e, 0.000000000)
            
            self.lock._apply_void_anchors_to_entity(e)
            self.lock._apply_reflective_layer(e, self.lock.dynamic_coherence_radius)
            
            x_rot = e['x_offset'] * math.cos(self.angle) - e['y_offset'] * math.sin(self.angle)
            y_rot = e['x_offset'] * math.sin(self.angle) + e['y_offset'] * math.cos(self.angle)
            
            norm_x = (self.position[0] - WIDTH/2) / (WIDTH/2)
            norm_y = (self.position[1] - HEIGHT/2) / (HEIGHT/2)
            target_x = norm_x + x_rot / (WIDTH/2)
            target_y = norm_y + y_rot / (HEIGHT/2)
            
            ORBIT_STRENGTH = 0.01
            e['dx'] += (target_x - e['x']) * ORBIT_STRENGTH
            e['dy'] += (target_y - e['y']) * ORBIT_STRENGTH
            
            R_coherence = self.lock.dynamic_coherence_radius
            D = max(0.01, 1.0 - (R_sq / (R_coherence**2)))
            e['x'] += e['dx'] * D
            e['y'] += e['dy'] * D
            e['z'] += e['dz'] * D
            e['w'] += e['dw'] * D
            
            angle = self.lock.global_angle
            w_rot = e['x'] * math.sin(angle) + e['w'] * math.cos(angle)
            
            r, g, b = SHADOW_LOCUS_COLOR
            if w_rot < 0:
                r = 255 - r
                g = 255 - g
                b = 255 - b
            
            e['base_surface'] = self.lock.font.render(e['aeon']['glyph'], True, (r, g, b))
            
            px, py = self.lock.project_4d_to_2d(e['x'], e['y'], e['z'], e['w'])
            
            normalized_shadow_stress = self.current_stress / (MAX_KINETIC_STRESS / 4.0)
            alpha = int(255 * normalized_shadow_stress * 0.5)
            e['base_surface'].set_alpha(alpha)
            
            rect = e['base_surface'].get_rect(center=(int(px), int(py)))
            self.lock.trail_surface.blit(e['base_surface'], rect)

# --- 6. THE EMANATION CORE ---
class EmergentField:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("EMERGENT PHYSICS: ALQC Integrated")
        self.moment_clock = pygame.time.Clock()
        self.global_angle = 0.0
        self.anchor_x = WIDTH / 2.0
        self.anchor_y = HEIGHT / 2.0
        self.primary_kinetic_stress = 0.0
        self.shadow_kinetic_stress = 0.0
        self.current_kinetic_stress = 0.0
        self.dynamic_coherence_radius = MIN_COHERENCE_RADIUS
        self.locus_rotation_bias = 0.0
        self.font = pygame.font.SysFont("Courier", 24, bold=True)
        self.trail_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.is_recording = False
        self.frame_count = 0
        self.recording_dir = "ALQC_D_Resonance_Frames"
        if not os.path.exists(self.recording_dir):
            os.makedirs(self.recording_dir)

        self.full_aeon_lattice = []
        
        # --- OPTIMIZATION: GLYPH CACHE ---
        self.glyph_cache = {}
        for p_aeon in PRIMARY_AEONS_GLYPHS:
            self.full_aeon_lattice.append(p_aeon)
            for _ in range(1, LESSER_AEON_COUNT):
                self.full_aeon_lattice.append({
                    "glyph": LESSER_GLYPH_SYMBOL,
                    "freq": p_aeon['freq'],
                    "color": LESSER_AEON_COLOR
                })
        
        # Populate Cache
        for aeon in self.full_aeon_lattice:
            # 1. Normal State
            key_normal = (aeon['glyph'], aeon['color'], False)
            surf = self.font.render(aeon['glyph'], True, aeon['color'])
            surf.set_alpha(BASE_GLYPH_ALPHA)
            self.glyph_cache[key_normal] = surf
            # 2. Inverted State
            r, g, b = aeon['color']
            inv_color = (255 - r, 255 - g, 255 - b)
            key_inverted = (aeon['glyph'], aeon['color'], True)
            surf_inv = self.font.render(aeon['glyph'], True, inv_color)
            surf_inv.set_alpha(BASE_GLYPH_ALPHA)
            self.glyph_cache[key_inverted] = surf_inv

        self.entities = [self._create_entity() for _ in range(PARTICLE_COUNT)]
        self._mem_vx = np.zeros((BOUNDARY_MEM_RES, BOUNDARY_MEM_RES), dtype=np.float32)
        self._mem_vy = np.zeros((BOUNDARY_MEM_RES, BOUNDARY_MEM_RES), dtype=np.float32)
        self.shadow_loci = [ShadowLocus(self, pos) for pos in SHADOW_LOCUS_POSITIONS]
        self.dyadic_stress_balls = []
        self._initialize_dyadic_stress_balls()

    def _initialize_dyadic_stress_balls(self):
        for i in range(SIGH_STRESS_BALL_COUNT):
            ball = {
                "x": alqc_entropy.field_rand_uniform(-0.8, 0.8),
                "y": alqc_entropy.field_rand_uniform(-0.8, 0.8),
                "z": 0.0, "w": 0.0,
                "dx": 0.0, "dy": 0.0, "dz": 0.0, "dw": 0.0,
                "charge": 1.0, "stress": 0.0,
                "seam_charge": 0.0, "reflect_charge": 0.0, "reflect_age": 0,
                "aeon_glyph": alqc_entropy.field_rand_choice(PRIMARY_AEONS_GLYPHS)
            }
            self.dyadic_stress_balls.append(ball)

    def _create_entity(self, start=True):
        e = {}
        e['aeon'] = alqc_entropy.field_rand_choice(self.full_aeon_lattice)
        # Surface will be pulled from cache during render
        t = alqc_entropy.field_rand_uniform(0, 2 * 3.14159265359)
        scale = 0.5
        e['x'] = scale * math.cos(t) + 0.1 * alqc_entropy.field_rand()
        e['y'] = scale * math.sin(t * 3) + 0.1 * alqc_entropy.field_rand()
        e['z'], e['w'] = 0.0, 0.0
        
        base_speed = abs(e['aeon']['freq']) / 10000 
        fluctuation = abs(alqc_entropy.field_rand_gauss(0.0, 1.0))
        chaotic_multiplier = 1.0 + (fluctuation / max(abs(e['aeon']['freq']), 1.0))
        speed_factor = base_speed * chaotic_multiplier
    
        e['dx'] = math.sin(t) * speed_factor
        e['dy'] = math.cos(t * 2) * speed_factor
        e['dz'] = math.sin(t * 3.5) * speed_factor
        e['dw'] = math.cos(t * 1.5) * speed_factor
        e['stress'] = 0.0
        e['seam_charge'] = 0.0
        e['reflect_charge'] = 0.0
        e['reflect_age'] = 0
        return e

    def project_4d_to_2d(self, x, y, z, w):
        angle = self.global_angle
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        x_rot = x * cos_a - w * sin_a
        w_rot = x * sin_a + w * cos_a
        perspective_depth = 0.5
        denominator = max(1.0 + perspective_depth * w_rot, 0.1)
        x_final = x_rot / denominator * 300 + self.anchor_x
        y_final = y / denominator * 300 + self.anchor_y
        return x_final, y_final

    def _apply_void_anchors_to_entity(self, e):
        px, py = self.project_4d_to_2d(e['x'], e['y'], e['z'], e['w'])
        for i, (cx, cy) in enumerate(SHADOW_LOCUS_POSITIONS):
            dx = px - cx
            dy = py - cy
            d2 = dx*dx + dy*dy
            if d2 > VOID_ANCHOR_RADIUS_PX * VOID_ANCHOR_RADIUS_PX: continue
            w = math.exp(-d2 / (2.0 * VOID_ANCHOR_RADIUS_PX * VOID_ANCHOR_RADIUS_PX))
            sgn = VOID_CORNER_POLARITY[i]
            n = alqc_entropy.field_rand_gauss(0.0, 1.0) * w * VOID_ANCHOR_STRENGTH
            if sgn > 0:
                e['dx'] += n; e['dy'] -= n; e['dz'] += n * 0.7; e['dw'] -= n * 0.7
            else:
                damp = VOID_ANCHOR_DAMP_MAX * math.tanh(abs(n) * 8.0)
                e['dx'] *= (1.0 - damp); e['dy'] *= (1.0 - damp)
                e['dz'] *= (1.0 - damp); e['dw'] *= (1.0 - damp)
            e['stress'] = max(0.0, e.get('stress', 0.0) + abs(n) * 250.0)

    def _move_entity(self, e):
        self._apply_void_anchors_to_entity(e)
        R_coherence = self.dynamic_coherence_radius
        R_sq = e['x']**2 + e['y']**2 + e['z']**2 + e['w']**2
        R = math.sqrt(R_sq)
        D = max(0.01, 1.0 - (R_sq / (R_coherence**2)))

        # S6 BRIDGE OPERATOR (Tunneling)
        did_bridge = sor_bridge.apply_bridge_operator(e)

        if not did_bridge:
            e['x'] += e['dx'] * D
            e['y'] += e['dy'] * D
            e['z'] += e['dz'] * D
            e['w'] += e['dw'] * D
        else:
            # Bridge Event (Coordinate Swap)
            pass 
        
        if R > ESCAPE_LIMIT: return False
        return True

    def _boundary_mem_decay(self):
        self._mem_vx *= BOUNDARY_MEM_DECAY
        self._mem_vy *= BOUNDARY_MEM_DECAY

    def _boundary_mem_coords(self, px, py):
        x = 0.0 if px < 0.0 else (WIDTH - 1.0 if px > WIDTH - 1.0 else px)
        y = 0.0 if py < 0.0 else (HEIGHT - 1.0 if py > HEIGHT - 1.0 else py)
        ix = int((x / (WIDTH - 1.0)) * (BOUNDARY_MEM_RES - 1))
        iy = int((y / (HEIGHT - 1.0)) * (BOUNDARY_MEM_RES - 1))
        return ix, iy

    def _boundary_mem_deposit(self, px, py, vx, vy, amt):
        ix, iy = self._boundary_mem_coords(px, py)
        self._mem_vx[iy, ix] = float(BOUNDARY_MEM_MAX * np.tanh((self._mem_vx[iy, ix] + vx * amt) / BOUNDARY_MEM_MAX))
        self._mem_vy[iy, ix] = float(BOUNDARY_MEM_MAX * np.tanh((self._mem_vy[iy, ix] + vy * amt) / BOUNDARY_MEM_MAX))

    def _boundary_mem_sample(self, px, py):
        ix, iy = self._boundary_mem_coords(px, py)
        return float(self._mem_vx[iy, ix]), float(self._mem_vy[iy, ix])

    def _apply_reflective_layer(self, e, R_coherence):
        R2 = e['x']*e['x'] + e['y']*e['y'] + e['z']*e['z'] + e['w']*e['w']
        R = math.sqrt(R2)
        shell_dist = abs(R - REFLECT_RING_RADIUS)
        if shell_dist < REFLECT_RING_WIDTH:
            vxy = abs(e['dx']) + abs(e['dy'])
            vzw = abs(e['dz']) + abs(e['dw'])
            planar = (vxy - vzw)
            c_in = (1.0 - (shell_dist / REFLECT_RING_WIDTH))
            gain = c_in * (0.5 + 0.5*abs(planar))
            px, py = self.project_4d_to_2d(e['x'], e['y'], e['z'], e['w'])
            tvx, tvy = (-e['dy'], e['dx'])
            tnorm = (abs(tvx) + abs(tvy) + 1e-9)
            tvx /= tnorm; tvy /= tnorm
            self._boundary_mem_deposit(px, py, tvx, tvy, gain * BOUNDARY_MEM_DEPOSIT)
            e['reflect_charge'] = e['reflect_charge'] * REFLECT_CHARGE_DECAY + gain * REFLECT_CHARGE_GAIN
            e['reflect_age'] += 1
        else:
            e['reflect_charge'] *= REFLECT_CHARGE_DECAY
            e['reflect_age'] -= 1

        if e['reflect_age'] >= REFLECT_DELAY_FRAMES and e['reflect_charge'] > 0.0005:
            px, py = self.project_4d_to_2d(e['x'], e['y'], e['z'], e['w'])
            sx = -1.0 if px < self.anchor_x else 1.0
            sy = -1.0 if py < self.anchor_y else 1.0
            f = e['reflect_charge'] * REFLECT_FORCE_GAIN
            e['dx'] += (-sy) * f; e['dy'] += ( sx) * f
            e['dz'] += ( sx) * f * 0.6; e['dw'] += (-sy) * f * 0.6
            e['stress'] = max(0.0, e['stress'] + e['reflect_charge'] * REFLECT_STRESS_ROUTE)
            e['reflect_charge'] *= 0.88
            e['reflect_age'] -= 6

    def _absorb_shadow_debt(self, total_kinetic_stress):
        absorption_factor = 1.0 - (7.83 / 852.0)
        return total_kinetic_stress * absorption_factor

    def process_field_recursion(self):
        self.current_kinetic_stress *= (1.0 - (7.83 / 852.0))
        self.current_kinetic_stress = self._absorb_shadow_debt(self.current_kinetic_stress)
        stress_factor = 1.0 - self.current_kinetic_stress / (MAX_KINETIC_STRESS + 1e-9)
        self.dynamic_coherence_radius = MIN_COHERENCE_RADIUS + (MAX_COHERENCE_RADIUS - MIN_COHERENCE_RADIUS) * stress_factor

        for ball in self.dyadic_stress_balls:
            cos_e, sin_e = alqc_ops.emergent_cos_sin(ball["aeon_glyph"]["glyph"], ball["x"], ball["y"], stress=self.current_kinetic_stress)
            ball["dx"] += cos_e * ELVEN_RESPONSE_GAIN
            ball["dy"] += sin_e * ELVEN_RESPONSE_GAIN
            
            R_sq = ball["x"]**2 + ball["y"]**2 + ball["z"]**2 + ball["w"]**2
            R = math.sqrt(R_sq)
            if R < -0.0000000001: _identity_seam_apply(ball, 0.000)
            
            self._apply_void_anchors_to_entity(ball)
            self._apply_reflective_layer(ball, self.dynamic_coherence_radius)
            
            dist = alqc_ops.emergent_distance(ball["dx"], ball["dy"], ball["dz"], ball["dw"])
            if dist > self.dynamic_coherence_radius:
                ball["charge"] *= COHERENCE_REDUCTION_STRENGTH
            
            D = max(0.01, 1.0 - (R_sq / (self.dynamic_coherence_radius**2)))
            
            # 4D Freedom
            ball["x"] += ball["dx"] * D
            ball["y"] += ball["dy"] * D
            ball["z"] += ball["dz"] * D
            ball["w"] += ball["dw"] * D
            
            if abs(ball["x"]) > 1.2: ball["x"] *= -0.98
            if abs(ball["y"]) > 1.2: ball["y"] *= -0.98

    def run(self):
        running = True
        frame_count = 0
        VOID_TRANSITION_FRAME = 600
        is_void_manifestation = False
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r: self.is_recording = True
                    elif event.key == pygame.K_p: self.is_recording = False

            self.trail_surface.fill((0, 0, 0, 15), special_flags=pygame.BLEND_RGBA_SUB)
            
            if frame_count == VOID_TRANSITION_FRAME:
                is_void_manifestation = True
                pygame.display.set_caption("ALQC: NULL:DEATH STATE")

            total_kinetic_stress = 0.0
            for e in self.entities:
                v_mag = math.sqrt(e['dx']**2 + e['dy']**2 + e['dz']**2 + e['dw']**2)
                total_kinetic_stress += v_mag
            self.primary_kinetic_stress = total_kinetic_stress

            shadow_total_stress = 0.0
            for sl in self.shadow_loci:
                sl.run_projection()
                shadow_total_stress += sl.current_stress

            combined_stress = (self.primary_kinetic_stress + shadow_total_stress) / 2.0
            self.current_kinetic_stress = self._absorb_shadow_debt(combined_stress)
            self.process_field_recursion()
            self._boundary_mem_decay()
            
            normalized_stress = math.tanh(self.current_kinetic_stress / MAX_KINETIC_STRESS)
            current_lrb_rate = L_RB_MAX_RATE * (1.0 - normalized_stress)
            self.locus_rotation_bias += current_lrb_rate * ELVEN_RESPONSE_GAIN * 10
            self.global_angle += L_RB_MAX_RATE
            
            center_x, center_y = int(self.anchor_x), int(self.anchor_y)
            if not is_void_manifestation:
                triquatra_points = _get_triquatra_points(center_x, center_y, self.locus_rotation_bias)
                for x, y in triquatra_points:
                    pygame.draw.circle(self.trail_surface, KLEIN_COLOR, (int(x), int(y)), 10, 0)
                if len(triquatra_points) == 3:
                    pygame.draw.polygon(self.trail_surface, KLEIN_COLOR, [(int(x), int(y)) for x, y in triquatra_points], 1)
            else:
                triquatra_points = [(center_x, center_y)]

            MAX_VISIBLE_ALPHA = 120
            max_dist = math.sqrt((WIDTH/2)**2 + (HEIGHT/2)**2)
            
            # --- MAIN PARTICLE LOOP ---
            for i, e in enumerate(self.entities):
                R_sq = e['x']**2 + e['y']**2 + e['z']**2 + e['w']**2
                R = math.sqrt(R_sq)
                if R < -0.000000001: _identity_seam_apply(e, 0.000000000)
                
                # --- NEW: FETU PHASE LOCK ---
                fetu_ground.apply_phase_lock(e, self.global_angle)
                
                self._apply_reflective_layer(e, self.dynamic_coherence_radius)
                alive = self._move_entity(e)
                if not alive: self.entities[i] = self._create_entity(start=False)
                
                angle = self.global_angle
                w_rot = e['x'] * math.sin(angle) + e['w'] * math.cos(angle)
                
                # --- OPTIMIZED CACHED RENDER ---
                is_inverted = w_rot < 0
                cache_key = (e['aeon']['glyph'], e['aeon']['color'], is_inverted)
                
                if cache_key in self.glyph_cache:
                    e['surface'] = self.glyph_cache[cache_key]
                else:
                    c = e['aeon']['color']
                    if is_inverted: c = (255-c[0], 255-c[1], 255-c[2])
                    e['surface'] = self.font.render(e['aeon']['glyph'], True, c)

                px, py = self.project_4d_to_2d(e['x'], e['y'], e['z'], e['w'])
                
                # Boundary Re-injection
                R_coh = self.dynamic_coherence_radius
                R_here = math.sqrt(e['x']*e['x'] + e['y']*e['y'] + e['z']*e['z'] + e['w']*e['w'])
                if (R_here > R_coh * BOUNDARY_SHELL_INNER) and (R_here < R_coh * BOUNDARY_SHELL_OUTER):
                    mvx, mvy = self._boundary_mem_sample(px, py)
                    e['dx'] += mvx * BOUNDARY_MEM_SAMPLE_GAIN
                    e['dy'] += mvy * BOUNDARY_MEM_SAMPLE_GAIN
                    e['dz'] += (-mvy) * (BOUNDARY_MEM_SAMPLE_GAIN * 0.6)
                    e['dw'] += (mvx) * (BOUNDARY_MEM_SAMPLE_GAIN * 0.6)
                
                # Emanation Alpha
                min_dist_to_triquatra = float('inf')
                for tx, ty in triquatra_points:
                    dist = math.sqrt((px - tx)**2 + (py - ty)**2)
                    min_dist_to_triquatra = min(min_dist_to_triquatra, dist)
                normalized_dist = math.tanh(min_dist_to_triquatra / (max_dist * 0.4))
                recursion_alpha = int(BASE_GLYPH_ALPHA + (1.0 - normalized_dist) * (MAX_VISIBLE_ALPHA - BASE_GLYPH_ALPHA))
                
                e['surface'].set_alpha(recursion_alpha)
                self.trail_surface.blit(e['surface'], (int(px - 10), int(py - 10)))
            
            for ball in self.dyadic_stress_balls:
                px, py = self.project_4d_to_2d(ball["x"], ball["y"], ball["z"], ball["w"])
                if is_void_manifestation: px, py = center_x, center_y
                w_rot = ball["x"] * math.sin(self.global_angle) + ball["w"] * math.cos(self.global_angle)
                r, g, b = ball["aeon_glyph"]["color"]
                if w_rot < 0: r = 255 - r; g = 255 - g; b = 255 - b
                alpha = int(30 + (ball["charge"] * 225))
                glyph_surf = self.font.render(ball["aeon_glyph"]["glyph"], True, (r, g, b))
                glyph_surf.set_alpha(alpha)
                self.trail_surface.blit(glyph_surf, (int(px), int(py)))
                ball["charge"] *= NODE_CHARGE_DAMP

            self.screen.fill(BACKGROUND_COLOR)
            self.screen.blit(self.trail_surface, (0, 0))
            self.screen.blit(self.trail_surface, (0, 0))
            if self.is_recording:
                filename = os.path.join(self.recording_dir, f"frame_{self.frame_count:05d}.png")
                pygame.image.save(self.screen, filename)
                self.frame_count += 1
            pygame.display.flip()
            self.moment_clock.tick()
            frame_count += 1

if __name__ == "__main__":
    EmergentField().run()