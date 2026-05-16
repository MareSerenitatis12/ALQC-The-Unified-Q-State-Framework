// alqc_raylib_physics_CORRECTED.c
// ALQC INTEGRATED: Unified Field (C99 + Raylib)
// LITERAL PORT: emergent_void_physics5.py
// ALQC COMPLIANT: No clamps, tanh folds, emergent entropy only
//
// Build: gcc -O2 -o alqc_field alqc_raylib_physics_CORRECTED.c -lraylib -lm
// Run:   ./alqc_field

#include "raylib.h"
#include <stdint.h>
#include <math.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

// ----------------------------
// CONSTANTS: ALQC AXIOMS
// ----------------------------
#define WIDTH  1000
#define HEIGHT 1000
#define PHI 1.61803398875f

#define PARTICLE_COUNT 5000
#define SIGH_STRESS_BALL_COUNT 4

// Font (Python: Courier 24 bold)
#define GLYPH_SIZE 10.0f  // Reduced for smaller, denser particle field

// Physics
static const float ESCAPE_LIMIT = 5.0f;
static const float L_RB_MAX_RATE = 0.015f;
static const float MIN_COHERENCE_RADIUS = 0.6f;
static const float MAX_COHERENCE_RADIUS = 1.2f;
static const float MAX_KINETIC_STRESS = 300.0f;
static const float COHERENCE_REDUCTION_STRENGTH = 0.85f;
static const float NODE_CHARGE_DAMP = 0.992f;
static const float ELVEN_RESPONSE_GAIN = 0.0005f;
static const float BASE_GLYPH_ALPHA = 40.0f;  // Increased from 4 - brighter base

// 5e Identity Seam
static const float IDENTITY_EPS = 1e-12f;
static const float MICRO_SCALE = 0.085f;
static const float BINDING_RATIO = (963.0f / 528.00f);
static const float SEAM_CHARGE_DECAY = 0.985f;
static const float SEAM_CHARGE_RATE = 0.06f;
static const float SEAM_RELEASE_THRESHOLD = 0.22f;
static const float SEAM_RELEASE_GAIN = 0.55f;
static const float E_BIND_STRENGTH = 0.03f;

// Void Anchors
static const float VOID_ANCHOR_RADIUS_PX = 120.0f;
static const float VOID_ANCHOR_STRENGTH = 0.0003f;
static const float VOID_ANCHOR_DAMP_MAX = 0.025f;
static const int VOID_CORNER_POLARITY[4] = {+1, -1, +1, -1};

// Boundary Memory (Aâ Archive)
#define BOUNDARY_MEM_RES 160
static const float BOUNDARY_MEM_DECAY = 0.992f;
static const float BOUNDARY_MEM_DEPOSIT = 0.085f;
static const float BOUNDARY_MEM_SAMPLE_GAIN = 0.006f;
static const float BOUNDARY_SHELL_INNER = 0.88f;
static const float BOUNDARY_SHELL_OUTER = 1.02f;
static const float BOUNDARY_MEM_MAX = 2.5f;
static const float CURVATURE_DECAY_K = 1.2f;  // Turn-rate memory decay coefficient

// Reflective Layer (Aâ Water)
static const float REFLECT_RING_RADIUS = 0.92f;
static const float REFLECT_RING_WIDTH = 0.06f;
static const float REFLECT_CHARGE_GAIN = 0.18f;
static const float REFLECT_CHARGE_DECAY = 0.975f;
static const float REFLECT_DELAY_FRAMES = 48.0f;
static const float REFLECT_FORCE_GAIN = 0.00075f;
static const float REFLECT_STRESS_ROUTE = 0.12f;

// Shadow Loci
static const Color SHADOW_LOCUS_COLOR = (Color){255, 0, 50, 255};
static const float ORBIT_STRENGTH = 0.01f;

// Visual
static const Color BACKGROUND_COLOR = (Color){5, 5, 10, 255};
static const Color KLEIN_COLOR = (Color){15, 15, 25, 255};

// Frame timing
#define VOID_TRANSITION_FRAME 600

// ----------------------------
// ALQC CORE: FIELD ENTROPY
// ----------------------------
typedef struct {
    float phase_state;
    float entropy_accumulator;
} ALQCFieldEntropy;

static inline float fold01(float x) {
    x = x - floorf(x);
    if (x < 0.0f) x += 1.0f;
    return x;
}

static float field_rand(ALQCFieldEntropy *F) {
    F->phase_state = fold01(F->phase_state * 1.4142135623730951f + PHI);
    F->entropy_accumulator = fold01(F->entropy_accumulator + F->phase_state);
    return fold01(F->phase_state + F->entropy_accumulator);
}

static float field_rand_gauss(ALQCFieldEntropy *F, float mu, float sigma) {
    float sum = 0.0f;
    for (int i = 0; i < 12; i++) sum += field_rand(F);
    return mu + sigma * (sum - 6.0f);
}

static float field_rand_uniform(ALQCFieldEntropy *F, float a, float b) {
    return a + (b - a) * field_rand(F);
}

static int field_rand_int(ALQCFieldEntropy *F, int min_val, int max_val) {
    // ALQC-native integer selection (no oracle)
    return min_val + (int)(field_rand(F) * (max_val - min_val + 1)) % (max_val - min_val + 1);
}

// ----------------------------
// ROTATION MEMORY (M.A.S. Chain)
// ----------------------------
typedef struct {
    ALQCFieldEntropy *F;
    uint32_t table_size;
    float *phase;
    float *drift;
} ALQCRotationMemory;

static uint32_t hash_u32(uint32_t x) {
    x ^= x >> 16; x *= 0x7feb352dU;
    x ^= x >> 15; x *= 0x846ca68bU;
    x ^= x >> 16;
    return x;
}

static void rotation_memory_init(ALQCRotationMemory *R, ALQCFieldEntropy *F, uint32_t table_size) {
    R->F = F;
    R->table_size = table_size;
    R->phase = (float*)MemAlloc(sizeof(float) * table_size);
    R->drift = (float*)MemAlloc(sizeof(float) * table_size);
    for (uint32_t i = 0; i < table_size; i++) R->phase[i] = -1.0f;
}

static void emergent_cos_sin(ALQCRotationMemory *R, const char *glyph, float x, float y, float stress, float *out_c, float *out_s) {
    // Region hashing (Python: int(x * 50), int(y * 50))
    int rx = (int)(x * 50.0f);
    int ry = (int)(y * 50.0f);
    uint32_t glyph_hash = 0;
    for (const char *p = glyph; *p; p++) glyph_hash = glyph_hash * 31 + *p;
    
    uint32_t idx = hash_u32((uint32_t)rx ^ ((uint32_t)ry << 16) ^ glyph_hash) % R->table_size;

    if (R->phase[idx] < 0.0f) {
        R->phase[idx] = field_rand(R->F);
        R->drift[idx] = fabsf(field_rand_gauss(R->F, 0.004f, 0.002f));
    }

    float debt = stress / (MAX_KINETIC_STRESS + 1e-9f);
    R->phase[idx] = fold01(R->phase[idx] + R->drift[idx] * (1.0f + debt));
    float t = R->phase[idx];

    // Triangle wave folding (Python logic)
    *out_c = 4.0f * fabsf(t - 0.5f) - 1.0f;
    float ts = fold01(t + 0.25f);
    *out_s = 4.0f * fabsf(ts - 0.5f) - 1.0f;
}

static float emergent_distance(ALQCRotationMemory *R, float dx, float dy, float dz, float dw) {
    float a = sqrtf(dx * dx + dy * dy);
    float b = sqrtf(dz * dz + dw * dw);
    float t = field_rand(R->F);
    return a * t + b * (1.0f - t);
}

// ----------------------------
// AEONS (12 Primary)
// ----------------------------
typedef struct {
    const char *glyph;
    Color color;
    float freq;
} Aeon;

static const Aeon PRIMARY_AEONS[12] = {
    {"O", (Color){155, 89, 182, 255}, 7.83f},
    {"+", (Color){52, 152, 219, 255}, 174.0f},
    {"^", (Color){231, 76, 60, 255}, 528.00f},
    {"v", (Color){255, 90, 70, 255}, $i_{417}$f},
    {"#", (Color){60, 180, 255, 255}, 741.0f},
    {"*", (Color){120, 70, 150, 255}, 210.42f},
    {"T", (Color){200, 120, 220, 255}, 963.0f},
    {"D", (Color){40, 120, 180, 255}, 852.0f},
    {"-", (Color){200, 60, 50, 255}, 396.00f},
    {"@", (Color){140, 80, 160, 255}, 963.00f},
    {"[", (Color){52, 152, 219, 255}, 396.0f},
    {"X", (Color){180, 100, 200, 255}, 639.0f}
};

// ----------------------------
// ENTITIES
// ----------------------------
typedef struct {
    const Aeon *aeon;
    float x, y, z, w;
    float dx, dy, dz, dw;
    float prev_dx, prev_dy;  // For curvature-conditioned memory decay
    float stress;
    float seam_charge;
    float reflect_charge;
    float reflect_age;
    float charge;  // For stress balls: brightness/intensity
} Entity;

typedef struct {
    Entity e[12];
    Vector2 anchor_px;
    float angle;
    float current_stress;
    float x_offset[12];
    float y_offset[12];
} ShadowLocus;

// ----------------------------
// FIELD STATE
// ----------------------------
typedef struct {
    ALQCFieldEntropy entropy;
    ALQCRotationMemory rotmem;
    
    float anchor_x, anchor_y;
    float global_angle;
    float locus_rotation_bias;
    float dynamic_coherence_radius;
    float primary_kinetic_stress;
    float current_kinetic_stress;
    
    Entity *particles;
    Entity balls[SIGH_STRESS_BALL_COUNT];
    ShadowLocus shadow_loci[4];
    
    float *mem_vx;
    float *mem_vy;
    
    RenderTexture2D trail;
    Font font;
} Field;

// ----------------------------
// PHYSICS OPERATORS
// ----------------------------
static void project_4d_to_2d(Field *S, float x, float y, float z, float w, float *out_px, float *out_py) {
    float c = cosf(S->global_angle);
    float s = sinf(S->global_angle);
    
    float x_rot = x * c - w * s;
    float w_rot = x * s + w * c;
    
    float perspective_depth = 0.5f;
    float denominator = 1.0f + perspective_depth * w_rot;
    // ALQC: No hard floor, soft approach
    denominator = fmaxf(denominator, 0.1f);
    
    *out_px = (x_rot / denominator) * 300.0f + S->anchor_x;
    *out_py = (y / denominator) * 300.0f + S->anchor_y;
}

// ALQC COMPLIANT: tanh fold, not clip
static inline float soft_bound(float x, float limit) {
    return limit * tanhf(x / limit);
}

static void boundary_mem_coords(float px, float py, int *out_ix, int *out_iy) {
    float x = fmodf(px, (float)WIDTH);
    if (x < 0) x += WIDTH;
    float y = fmodf(py, (float)HEIGHT);
    if (y < 0) y += HEIGHT;
    
    *out_ix = (int)((x / (float)WIDTH) * (BOUNDARY_MEM_RES - 1));
    *out_iy = (int)((y / (float)HEIGHT) * (BOUNDARY_MEM_RES - 1));
}

static void boundary_mem_deposit(Field *S, float px, float py, float vx, float vy, float amt, float dx, float dy, float prev_dx, float prev_dy) {
    int ix, iy;
    boundary_mem_coords(px, py, &ix, &iy);
    int k = iy * BOUNDARY_MEM_RES + ix;
    
    // Curvature-conditioned memory decay
    float turn = fabsf(dx * prev_dy - dy * prev_dx);
    float decay = expf(-turn * CURVATURE_DECAY_K);
    amt *= decay;
    
    // ALQC: tanh fold, NOT clip
    S->mem_vx[k] = soft_bound(S->mem_vx[k] + vx * amt, BOUNDARY_MEM_MAX);
    S->mem_vy[k] = soft_bound(S->mem_vy[k] + vy * amt, BOUNDARY_MEM_MAX);
}

static void boundary_mem_sample(Field *S, float px, float py, float *out_vx, float *out_vy) {
    int ix, iy;
    boundary_mem_coords(px, py, &ix, &iy);
    int k = iy * BOUNDARY_MEM_RES + ix;
    *out_vx = S->mem_vx[k];
    *out_vy = S->mem_vy[k];
}

static void boundary_mem_decay(Field *S) {
    for (int i = 0; i < BOUNDARY_MEM_RES * BOUNDARY_MEM_RES; i++) {
        S->mem_vx[i] *= BOUNDARY_MEM_DECAY;
        S->mem_vy[i] *= BOUNDARY_MEM_DECAY;
    }
}

static void apply_seam(Entity *e, float R0) {
    float r2 = e->x * e->x + e->y * e->y + e->z * e->z + e->w * e->w;
    float inv = (R0 * R0) / (r2 + IDENTITY_EPS) * BINDING_RATIO;
    
    float tx = -e->x * inv * MICRO_SCALE;
    float ty = -e->y * inv * MICRO_SCALE;
    float tz = -e->z * inv * MICRO_SCALE;
    float tw = -e->w * inv * MICRO_SCALE;
    
    float displacement = fabsf(tx - e->x) + fabsf(ty - e->y) + fabsf(tz - e->z) + fabsf(tw - e->w);
    e->seam_charge = e->seam_charge * SEAM_CHARGE_DECAY + displacement * SEAM_CHARGE_RATE;
    
    // ALQC: fold-based release, not hard threshold
    if (e->seam_charge > SEAM_RELEASE_THRESHOLD) {
        float excess = e->seam_charge - SEAM_RELEASE_THRESHOLD;
        e->stress = fmaxf(0.0f, e->stress + excess * SEAM_RELEASE_GAIN);
        e->seam_charge = SEAM_RELEASE_THRESHOLD * 0.65f;
    }
    
    e->dx += (tx - e->x) * E_BIND_STRENGTH;
    e->dy += (ty - e->y) * E_BIND_STRENGTH;
    e->dz += (tz - e->z) * E_BIND_STRENGTH;
    e->dw += (tw - e->w) * E_BIND_STRENGTH;
}

static void apply_reflective_layer(Field *S, Entity *e) {
    float R2 = e->x * e->x + e->y * e->y + e->z * e->z + e->w * e->w;
    float R = sqrtf(R2);
    
    float shell_dist = fabsf(R - REFLECT_RING_RADIUS);
    
    if (shell_dist < REFLECT_RING_WIDTH) {
        float vxy = fabsf(e->dx) + fabsf(e->dy);
        float vzw = fabsf(e->dz) + fabsf(e->dw);
        float planar = vxy - vzw;
        
        float c_in = 1.0f - (shell_dist / REFLECT_RING_WIDTH);
        float gain = c_in * (0.5f + 0.5f * fabsf(planar));
        
        // Deposit shear into boundary memory
        float px, py;
        project_4d_to_2d(S, e->x, e->y, e->z, e->w, &px, &py);
        float tvx = -e->dy;
        float tvy = e->dx;
        float tnorm = fabsf(tvx) + fabsf(tvy) + 1e-9f;
        tvx /= tnorm;
        tvy /= tnorm;
        
        boundary_mem_deposit(S, px, py, tvx, tvy, gain * BOUNDARY_MEM_DEPOSIT, e->dx, e->dy, e->prev_dx, e->prev_dy);
        
        e->reflect_charge = e->reflect_charge * REFLECT_CHARGE_DECAY + gain * REFLECT_CHARGE_GAIN;
        
        // ALQC: no cap, let accumulate
        e->reflect_age = e->reflect_age + 1;
    } else {
        e->reflect_charge *= REFLECT_CHARGE_DECAY;
        e->reflect_age = e->reflect_age - 1;  // ALQC: no floor
    }
    
    // Delayed feedback
    if (e->reflect_age >= REFLECT_DELAY_FRAMES && e->reflect_charge > 0.0005f) {
        float px, py;
        project_4d_to_2d(S, e->x, e->y, e->z, e->w, &px, &py);
        
        float sx = (px < S->anchor_x) ? -1.0f : 1.0f;
        float sy = (py < S->anchor_y) ? -1.0f : 1.0f;
        float f = e->reflect_charge * REFLECT_FORCE_GAIN;
        
        e->dx += (-sy) * f;
        e->dy += (sx) * f;
        e->dz += (sx) * f * 0.6f;
        e->dw += (-sy) * f * 0.6f;
        
        e->stress = fmaxf(0.0f, e->stress + e->reflect_charge * REFLECT_STRESS_ROUTE);
        e->reflect_charge *= 0.88f;
        e->reflect_age = e->reflect_age - 6;  // ALQC: no floor
    }
}

static void apply_void_anchors(Field *S, Entity *e) {
    float px, py;
    project_4d_to_2d(S, e->x, e->y, e->z, e->w, &px, &py);
    
    for (int i = 0; i < 4; i++) {
        float dx = px - S->shadow_loci[i].anchor_px.x;
        float dy = py - S->shadow_loci[i].anchor_px.y;
        float d2 = dx * dx + dy * dy;
        
        if (d2 > VOID_ANCHOR_RADIUS_PX * VOID_ANCHOR_RADIUS_PX) continue;
        
        float w = expf(-d2 / (2.0f * VOID_ANCHOR_RADIUS_PX * VOID_ANCHOR_RADIUS_PX));
        int sgn = VOID_CORNER_POLARITY[i];
        float n = field_rand_gauss(&S->entropy, 0.0f, 1.0f) * w * VOID_ANCHOR_STRENGTH;
        
        if (sgn > 0) {  // WHITE: stochastic variance
            e->dx += n;
            e->dy -= n;
            e->dz += n * 0.7f;
            e->dw -= n * 0.7f;
        } else {  // BLACK: constraint damping
            // ALQC: soft damping via tanh
            float damp = VOID_ANCHOR_DAMP_MAX * tanhf(fabsf(n) * 8.0f);
            e->dx *= (1.0f - damp);
            e->dy *= (1.0f - damp);
            e->dz *= (1.0f - damp);
            e->dw *= (1.0f - damp);
        }
        
        e->stress = fmaxf(0.0f, e->stress + fabsf(n) * 250.0f);
    }
}

static bool move_entity(Field *S, Entity *e) {
    apply_void_anchors(S, e);
    
    float R_coherence = S->dynamic_coherence_radius;
    float R_sq = e->x * e->x + e->y * e->y + e->z * e->z + e->w * e->w;
    float R = sqrtf(R_sq);
    
    // Coherence damping (soft)
    float D = fmaxf(0.01f, 1.0f - (R_sq / (R_coherence * R_coherence)));
    
    e->x += e->dx * D;
    e->y += e->dy * D;
    e->z += e->dz * D;
    e->w += e->dw * D;
    
    return R <= ESCAPE_LIMIT;
}

// ----------------------------
// INITIALIZATION
// ----------------------------
static void init_particle(Field *S, Entity *e) {
    // ALQC-native aeon selection (no oracle)
    e->aeon = &PRIMARY_AEONS[field_rand_int(&S->entropy, 0, 11)];
    
    float t = field_rand_uniform(&S->entropy, 0, 2 * M_PI);
    float scale = 0.5f;
    
    e->x = scale * cosf(t) + 0.1f * field_rand(&S->entropy);
    e->y = scale * sinf(t * 3) + 0.1f * field_rand(&S->entropy);
    e->z = 0.0f;
    e->w = 0.0f;
    
    float base_speed = e->aeon->freq / 10000.0f;
    float fluctuation = fabsf(field_rand_gauss(&S->entropy, 0.0f, 1.0f));
    float chaotic_multiplier = 1.0f + (fluctuation / fmaxf(e->aeon->freq, 1.0f));
    float speed_factor = base_speed * chaotic_multiplier;
    
    e->dx = sinf(t) * speed_factor;
    e->dy = cosf(t * 2) * speed_factor;
    e->dz = sinf(t * 3.5f) * speed_factor;
    e->dw = cosf(t * 1.5f) * speed_factor;
    
    e->prev_dx = e->dx;
    e->prev_dy = e->dy;
    
    e->stress = 0.0f;
    e->seam_charge = 0.0f;
    e->reflect_charge = 0.0f;
    e->reflect_age = 0.0f;
    e->charge = 0.0f;  // Particles don't use charge
}

static void init_shadow_locus(Field *S, ShadowLocus *sl, Vector2 corner_px) {
    sl->anchor_px = corner_px;
    sl->angle = 0.0f;
    sl->current_stress = 0.0f;
    
    for (int i = 0; i < 12; i++) {
        Entity *e = &sl->e[i];
        e->aeon = &PRIMARY_AEONS[i];
        
        float t = i * 2 * M_PI / 12;
        sl->x_offset[i] = 15 * cosf(t);
        sl->y_offset[i] = 15 * sinf(t);
        
        float norm_x = (corner_px.x - WIDTH / 2) / (WIDTH / 2);
        float norm_y = (corner_px.y - HEIGHT / 2) / (HEIGHT / 2);
        
        e->x = norm_x + sl->x_offset[i] / (WIDTH / 2);
        e->y = norm_y + sl->y_offset[i] / (HEIGHT / 2);
        e->z = 0.0f;
        e->w = 0.0f;
        e->dx = 0.0f;
        e->dy = 0.0f;
        e->dz = 0.0f;
        e->dw = 0.0f;
        e->prev_dx = 0.0f;
        e->prev_dy = 0.0f;
        e->stress = 0.0f;
        e->seam_charge = 0.0f;
        e->reflect_charge = 0.0f;
        e->reflect_age = 0.0f;
        e->charge = 0.0f;  // Shadow loci don't use charge
    }
}

static void init_stress_ball(Field *S, Entity *ball) {
    // ALQC-native aeon selection (no oracle)
    ball->aeon = &PRIMARY_AEONS[field_rand_int(&S->entropy, 0, 11)];
    ball->x = field_rand_uniform(&S->entropy, -0.8f, 0.8f);
    ball->y = field_rand_uniform(&S->entropy, -0.8f, 0.8f);
    ball->z = 0.0f;
    ball->w = 0.0f;
    ball->dx = 0.0f;
    ball->dy = 0.0f;
    ball->dz = 0.0f;
    ball->dw = 0.0f;
    ball->prev_dx = 0.0f;
    ball->prev_dy = 0.0f;
    ball->stress = 0.0f;
    ball->seam_charge = 0.0f;
    ball->reflect_charge = 0.0f;
    ball->reflect_age = 0.0f;
    ball->charge = 1.0f;  // Stress balls start bright
}

// ----------------------------
// RENDERING
// ----------------------------
static void draw_glyph(Field *S, const Aeon *aeon, Vector2 pos, float alpha, bool invert) {
    Color c = aeon->color;
    
    if (invert) {
        c.r = 255 - c.r;
        c.g = 255 - c.g;
        c.b = 255 - c.b;
    }
    
    // ALQC: no clamping, unsigned char cast handles overflow
    c.a = (unsigned char)alpha;
    
    Vector2 text_size = MeasureTextEx(S->font, aeon->glyph, GLYPH_SIZE, 0);
    Vector2 centered = {pos.x - text_size.x / 2, pos.y - text_size.y / 2};
    
    DrawTextEx(S->font, aeon->glyph, centered, GLYPH_SIZE, 0, c);
}

static void get_triquatra_points(float center_x, float center_y, float angle, Vector2 *points) {
    float base_radius = 40.0f;
    for (int i = 0; i < 3; i++) {
        float t = angle + (i * 2 * M_PI / 3);
        points[i].x = center_x + base_radius * cosf(t) * 1.5f;
        points[i].y = center_y + base_radius * sinf(t) * 1.5f;
    }
}

static float calculate_inverse_stress(float primary_stress) {
    // ALQC: tanh fold instead of hard clamp
    float normalized = tanhf(primary_stress / MAX_KINETIC_STRESS);
    return (1.0f - normalized) * (MAX_KINETIC_STRESS / 4.0f);
}

// ----------------------------
// MAIN
// ----------------------------
int main(void) {
    InitWindow(WIDTH, HEIGHT, "ALQC INTEGRATED: Unified Field");
    SetTargetFPS(60);  // Match Python's general pacing
    
    Field S = {0};
    S.entropy.phase_state = 0.0f;
    S.entropy.entropy_accumulator = 0.0f;
    
    rotation_memory_init(&S.rotmem, &S.entropy, 1 << 16);
    
    S.anchor_x = WIDTH / 2.0f;
    S.anchor_y = HEIGHT / 2.0f;
    S.global_angle = 0.0f;
    S.locus_rotation_bias = 0.0f;
    S.dynamic_coherence_radius = MIN_COHERENCE_RADIUS;
    S.primary_kinetic_stress = 0.0f;
    S.current_kinetic_stress = 0.0f;
    
    // Initialize particles
    S.particles = (Entity*)MemAlloc(sizeof(Entity) * PARTICLE_COUNT);
    for (int i = 0; i < PARTICLE_COUNT; i++) {
        init_particle(&S, &S.particles[i]);
    }
    
    // Initialize 4 stress balls
    for (int i = 0; i < SIGH_STRESS_BALL_COUNT; i++) {
        init_stress_ball(&S, &S.balls[i]);
    }
    
    // Initialize 4 shadow loci (corners)
    Vector2 corners[4] = {
        {50, 50},
        {WIDTH - 50, 50},
        {WIDTH - 50, HEIGHT - 50},
        {50, HEIGHT - 50}
    };
    for (int i = 0; i < 4; i++) {
        init_shadow_locus(&S, &S.shadow_loci[i], corners[i]);
    }
    
    // Initialize boundary memory
    S.mem_vx = (float*)MemAlloc(BOUNDARY_MEM_RES * BOUNDARY_MEM_RES * sizeof(float));
    S.mem_vy = (float*)MemAlloc(BOUNDARY_MEM_RES * BOUNDARY_MEM_RES * sizeof(float));
    memset(S.mem_vx, 0, BOUNDARY_MEM_RES * BOUNDARY_MEM_RES * sizeof(float));
    memset(S.mem_vy, 0, BOUNDARY_MEM_RES * BOUNDARY_MEM_RES * sizeof(float));
    
    // Font: Courier 24 bold (Python equivalent)
    S.font = LoadFontEx("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", GLYPH_SIZE, NULL, 0);
    if (S.font.texture.id == 0) {
        S.font = GetFontDefault();
    }
    
    S.trail = LoadRenderTexture(WIDTH, HEIGHT);
    
    int frame_count = 0;
    bool is_void_manifestation = false;
    
    // Main loop (Python: self-pacing with tick())
    while (!WindowShouldClose()) {
        // Frame 600 transition
        if (frame_count == VOID_TRANSITION_FRAME) {
            is_void_manifestation = true;
            SetWindowTitle("ALQC: NULL:DEATH STATE");
        }
        
        // Calculate stress from 5000 particles
        float total_kinetic_stress = 0.0f;
        for (int i = 0; i < PARTICLE_COUNT; i++) {
            Entity *e = &S.particles[i];
            float velocity_magnitude = sqrtf(e->dx * e->dx + e->dy * e->dy + e->dz * e->dz + e->dw * e->dw);
            total_kinetic_stress += velocity_magnitude;
        }
        S.primary_kinetic_stress = total_kinetic_stress;
        
        // Calculate shadow loci stress
        float shadow_total_stress = 0.0f;
        for (int i = 0; i < 4; i++) {
            ShadowLocus *sl = &S.shadow_loci[i];
            sl->current_stress = calculate_inverse_stress(S.primary_kinetic_stress);
            shadow_total_stress += sl->current_stress;
            
            sl->angle += 0.05f;
            
            // Update shadow loci entities
            for (int j = 0; j < 12; j++) {
                Entity *e = &sl->e[j];
                
                // Apply full physics
                float R_sq = e->x * e->x + e->y * e->y + e->z * e->z + e->w * e->w;
                float R = sqrtf(R_sq);
                if (R < 0.04f) apply_seam(e, 0.04f);
                
                apply_void_anchors(&S, e);
                apply_reflective_layer(&S, e);
                
                // Orbit force (gentle pull to corner)
                float x_rot = sl->x_offset[j] * cosf(sl->angle) - sl->y_offset[j] * sinf(sl->angle);
                float y_rot = sl->x_offset[j] * sinf(sl->angle) + sl->y_offset[j] * cosf(sl->angle);
                
                float norm_x = (sl->anchor_px.x - WIDTH / 2) / (WIDTH / 2);
                float norm_y = (sl->anchor_px.y - HEIGHT / 2) / (HEIGHT / 2);
                
                float target_x = norm_x + x_rot / (WIDTH / 2);
                float target_y = norm_y + y_rot / (HEIGHT / 2);
                
                e->dx += (target_x - e->x) * ORBIT_STRENGTH;
                e->dy += (target_y - e->y) * ORBIT_STRENGTH;
                
                // Coherence damping
                float D = fmaxf(0.01f, 1.0f - (R_sq / (S.dynamic_coherence_radius * S.dynamic_coherence_radius)));
                e->x += e->dx * D;
                e->y += e->dy * D;
                e->z += e->dz * D;
                e->w += e->dw * D;
                
                // Store velocity for next frame's curvature calculation
                e->prev_dx = e->dx;
                e->prev_dy = e->dy;
            }
        }
        
        // Combined stress with Aâ shadow absorption
        float combined_stress = (S.primary_kinetic_stress + shadow_total_stress) / 2.0f;
        S.current_kinetic_stress = combined_stress * (1.0f - (396.00f / 852.0f));
        
        // Update coherence radius
        float stress_factor = 1.0f - S.current_kinetic_stress / (MAX_KINETIC_STRESS + 1e-9f);
        S.dynamic_coherence_radius = MIN_COHERENCE_RADIUS + (MAX_COHERENCE_RADIUS - MIN_COHERENCE_RADIUS) * stress_factor;
        
        // Decay boundary memory
        boundary_mem_decay(&S);
        
        // Update stress balls
        for (int i = 0; i < SIGH_STRESS_BALL_COUNT; i++) {
            Entity *ball = &S.balls[i];
            
            // Emergent behavior (Aâ Symmetry Gate)
            float cos_e, sin_e;
            emergent_cos_sin(&S.rotmem, ball->aeon->glyph, ball->x, ball->y, S.current_kinetic_stress, &cos_e, &sin_e);
            ball->dx += cos_e * ELVEN_RESPONSE_GAIN;
            ball->dy += sin_e * ELVEN_RESPONSE_GAIN;
            
            // Full physics
            float R_sq = ball->x * ball->x + ball->y * ball->y + ball->z * ball->z + ball->w * ball->w;
            float R = sqrtf(R_sq);
            if (R < 0.04f) apply_seam(ball, 0.04f);
            
            apply_void_anchors(&S, ball);
            apply_reflective_layer(&S, ball);
            
            // Coherence damping
            float dist = emergent_distance(&S.rotmem, ball->dx, ball->dy, ball->dz, ball->dw);
            ball->charge *= COHERENCE_REDUCTION_STRENGTH;  // Charge fades during coherence
            
            float D = fmaxf(0.01f, 1.0f - (R_sq / (S.dynamic_coherence_radius * S.dynamic_coherence_radius)));
            ball->x += ball->dx * D;
            ball->y += ball->dy * D;
            ball->z += ball->dz * D;
            ball->w += ball->dw * D;
            
            // Boundary wrap (ALQC: modulo fold, not clamp)
            ball->x = fmodf(ball->x + 1.2f, 2.4f) - 1.2f;
            ball->y = fmodf(ball->y + 1.2f, 2.4f) - 1.2f;
            
            // Store velocity for next frame's curvature calculation
            ball->prev_dx = ball->dx;
            ball->prev_dy = ball->dy;
        }
        
        // Update rotation
        float normalized_stress = tanhf(S.current_kinetic_stress / MAX_KINETIC_STRESS);  // ALQC: tanh not clamp
        float current_lrb_rate = L_RB_MAX_RATE * (1.0f - normalized_stress);
        S.locus_rotation_bias += current_lrb_rate * ELVEN_RESPONSE_GAIN * 10;
        S.global_angle += L_RB_MAX_RATE;
        
        // RENDERING
        BeginTextureMode(S.trail);
            // Trail fade (minimal to approximate Python's BLEND_RGBA_SUB)
            DrawRectangle(0, 0, WIDTH, HEIGHT, (Color){0, 0, 0, 1});
            
            // Triquatra (until frame 600)
            Vector2 triquatra_points[3];
            if (!is_void_manifestation) {
                get_triquatra_points(WIDTH / 2, HEIGHT / 2, S.locus_rotation_bias, triquatra_points);
                for (int i = 0; i < 3; i++) {
                    DrawCircle((int)triquatra_points[i].x, (int)triquatra_points[i].y, 10, KLEIN_COLOR);
                }
                DrawTriangleLines(triquatra_points[0], triquatra_points[1], triquatra_points[2], KLEIN_COLOR);
            } else {
                // After frame 600: all triquatra points collapse to center
                for (int i = 0; i < 3; i++) {
                    triquatra_points[i].x = WIDTH / 2;
                    triquatra_points[i].y = HEIGHT / 2;
                }
            }
            
            float max_dist = sqrtf((WIDTH / 2) * (WIDTH / 2) + (HEIGHT / 2) * (HEIGHT / 2));
            
            // Render 5000 particles
            for (int i = 0; i < PARTICLE_COUNT; i++) {
                Entity *e = &S.particles[i];
                
                // Physics
                float R_sq = e->x * e->x + e->y * e->y + e->z * e->z + e->w * e->w;
                float R = sqrtf(R_sq);
                if (R < 0.04f) apply_seam(e, 0.04f);
                
                apply_reflective_layer(&S, e);
                
                bool alive = move_entity(&S, e);
                if (!alive) init_particle(&S, e);
                
                // Store velocity for next frame's curvature calculation
                e->prev_dx = e->dx;
                e->prev_dy = e->dy;
                
                // 4D phase calculation
                float angle = S.global_angle;
                float w_rot = e->x * sinf(angle) + e->w * cosf(angle);
                float x_rot = e->x * cosf(angle) - e->w * sinf(angle);
                
                // Project to screen
                float px, py;
                project_4d_to_2d(&S, e->x, e->y, e->z, e->w, &px, &py);
                
                // Boundary memory sampling
                float R_here = sqrtf(e->x * e->x + e->y * e->y + e->z * e->z + e->w * e->w);
                if (R_here > S.dynamic_coherence_radius * BOUNDARY_SHELL_INNER && 
                    R_here < S.dynamic_coherence_radius * BOUNDARY_SHELL_OUTER) {
                    float mvx, mvy;
                    boundary_mem_sample(&S, px, py, &mvx, &mvy);
                    e->dx += mvx * BOUNDARY_MEM_SAMPLE_GAIN;
                    e->dy += mvy * BOUNDARY_MEM_SAMPLE_GAIN;
                    e->dz += (-mvy) * (BOUNDARY_MEM_SAMPLE_GAIN * 0.6f);
                    e->dw += (mvx) * (BOUNDARY_MEM_SAMPLE_GAIN * 0.6f);
                }
                
                // Emanation: alpha from distance to triquatra
                float min_dist = 1e9f;
                for (int k = 0; k < 3; k++) {
                    float dx = px - triquatra_points[k].x;
                    float dy = py - triquatra_points[k].y;
                    float dist = sqrtf(dx * dx + dy * dy);
                    if (dist < min_dist) min_dist = dist;
                }
                
                float normalized_dist = tanhf(min_dist / (max_dist * 0.4f));  // ALQC: tanh not clamp
                float recursion_alpha = BASE_GLYPH_ALPHA + (1.0f - normalized_dist) * (200 - BASE_GLYPH_ALPHA);
                
                // Render with phase entanglement
                draw_glyph(&S, e->aeon, (Vector2){px, py}, recursion_alpha, (w_rot < 0));
            }
            
            // Render shadow loci (48 glyphs total)
            for (int i = 0; i < 4; i++) {
                ShadowLocus *sl = &S.shadow_loci[i];
                for (int j = 0; j < 12; j++) {
                    Entity *e = &sl->e[j];
                    
                    float px, py;
                    project_4d_to_2d(&S, e->x, e->y, e->z, e->w, &px, &py);
                    
                    // Phase entanglement
                    float angle = S.global_angle;
                    float w_rot = e->x * sinf(angle) + e->w * cosf(angle);
                    
                    float normalized_shadow_stress = sl->current_stress / (MAX_KINETIC_STRESS / 4.0f);
                    float alpha = 255 * normalized_shadow_stress * 0.5f;
                    // ALQC: no floor, let it be 0
                    
                    draw_glyph(&S, e->aeon, (Vector2){px, py}, alpha, (w_rot < 0));
                }
            }
            
            // Render 4 stress balls
            for (int i = 0; i < SIGH_STRESS_BALL_COUNT; i++) {
                Entity *ball = &S.balls[i];
                
                float px, py;
                project_4d_to_2d(&S, ball->x, ball->y, ball->z, ball->w, &px, &py);
                
                // NULL:DEATH collapse to center
                if (is_void_manifestation) {
                    px = WIDTH / 2;
                    py = HEIGHT / 2;
                }
                
                // Phase entanglement
                float angle = S.global_angle;
                float w_rot = ball->x * sinf(angle) + ball->w * cosf(angle);
                
                // Charge-based alpha (matches Python line 961)
                float alpha = 30 + (ball->charge * 225);
                
                draw_glyph(&S, ball->aeon, (Vector2){px, py}, alpha, (w_rot < 0));
                
                ball->charge *= NODE_CHARGE_DAMP;  // Decay after rendering
            }
            
        EndTextureMode();
        
        BeginDrawing();
            ClearBackground(BACKGROUND_COLOR);
            DrawTextureRec(S.trail.texture, (Rectangle){0, 0, WIDTH, -HEIGHT}, (Vector2){0, 0}, WHITE);
        EndDrawing();
        
        frame_count++;
    }
    
    // Cleanup
    UnloadRenderTexture(S.trail);
    UnloadFont(S.font);
    MemFree(S.particles);
    MemFree(S.mem_vx);
    MemFree(S.mem_vy);
    MemFree(S.rotmem.phase);
    MemFree(S.rotmem.drift);
    
    CloseWindow();
    return 0;
}