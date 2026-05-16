

# APPENDIX Q: THE RAYLIB VISUALIZATION KERNEL (Source Code)
 [Ref: appendixQ]

The Visual Proof: This kernel (textttalqcraylib\âhysics18.cpp) handles the "Manifestation Layer." It translates the mathematical vectors of the engine into the superpositioned visual data observed by the Magus. It enforces the 110-Limit and the Additive Blending modes required for the Holographic Proof.

[language=C++, basicstyle=tinyttfamily, breaklines=true]
// alqcraylibâhysicsCORRECTED.c
// ALQC INTEGRATED: Unified Field (C99 + Raylib)
// LITERAL PORT: emergentvoidâhysics5.py
// ALQC COMPLIANT: No clamps, tanh folds, emergent entropy only
//
// Build: gcc -O2 -o alqcfield alqcraylibâhysicsCORRECTED.c -lraylib -lm
// Run:   ./alqcfield

#include "raylib.h"
#include <stdint.h>
#include <math.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>

#ifndef MPI
#define MPI 3.14159265358979323846
#endif

// ----------------------------
// CONSTANTS: ALQC AXIOMS
// ----------------------------
#define WIDTH  1000
#define HEIGHT 1000
#define PHI 1.61803398875f

#define PARTICLECOUNT 5000
#define SIGHSTRESSBALLCOUNT 4

// Font (Python: Courier 24 bold)
#define GLYPHSIZE 10.0f  // Reduced for smaller, denser particle field

// Physics
static const float ESCAPELIMIT = 5.0f;
static const float LRBMAXRATE = 0.015f;
static const float MINCOHERENCERADIUS = 0.6f;
static const float MAXCOHERENCERADIUS = 1.2f;
static const float MAXKINETICSTRESS = 300.0f;
static const float COHERENCEREDUCTIONSTRENGTH = 0.85f;
static const float NODECHARGEDAMP = 0.992f;
static const float ELVENRESPONSEGAIN = 0.0005f;
static const float BASEGLYPHALPHA = 40.0f;  // Increased from 4 - brighter base

// 5e Identity Seam
static const float IDENTITYEPS = 1e-12f;
static const float MICROSCALE = 0.085f;
static const float BINDINGRATIO = (963.0f / 528.00f);
static const float SEAMCHARGEDECAY = 0.985f;
static const float SEAMCHARGERATE = 0.06f;
static const float SEAMRELEASETHRESHOLD = 0.22f;
static const float SEAMRELEASEGAIN = 0.55f;
static const float EBINDSTRENGTH = 0.03f;

// Void Anchors
static const float VOIDANCHORRADIUSPX = 120.0f;
static const float VOIDANCHORSTRENGTH = 0.0003f;
static const float VOIDANCHORDAMPMAX = 0.025f;
static const int VOIDCORNERPOLARITY[4] = +1, -1, +1, -1;

// Boundary Memory (Aâ Archive)
#define BOUNDARYMEMRES 160
static const float BOUNDARYMEMDECAY = 0.992f;
static const float BOUNDARYMEMDEPOSIT = 0.085f;
static const float BOUNDARYMEMSAMPLEGAIN = 0.006f;
static const float BOUNDARYSHELLINNER = 0.88f;
static const float BOUNDARYSHELLOUTER = 1.02f;
static const float BOUNDARYMEMMAX = 2.5f;
static const float CURVATUREDECAYK = 1.2f;  // Turn-rate memory decay coefficient

// Reflective Layer (Aâ Water)
static const float REFLECTRINGRADIUS = 0.92f;
static const float REFLECTRINGWIDTH = 0.06f;
static const float REFLECTCHARGEGAIN = 0.18f;
static const float REFLECTCHARGEDECAY = 0.975f;
static const float REFLECTDELAYFRAMES = 48.0f;
static const float REFLECTFORCEGAIN = 0.00075f;
static const float REFLECTSTRESSROUTE = 0.12f;

// Shadow Loci
static const Color SHADOWLOCUSCOLOR = (Color)255, 0, 50, 255;
static const float ORBITSTRENGTH = 0.01f;

// Visual
static const Color BACKGROUNDCOLOR = (Color)5, 5, 10, 255;
static const Color KLEINCOLOR = (Color)15, 15, 25, 255;

// Frame timing
#define VOIDTRANSITIONFRAME 600

// ----------------------------
// ALQC CORE: FIELD ENTROPY
// ----------------------------
typedef struct 
    float phaseâtate;
    float entropyâccumulator;
 ALQCFieldEntropy;

static inline float fold01(float x) 
    x = x - floorf(x);
    if (x < 0.0f) x += 1.0f;
    return x;

static float fieldrand(ALQCFieldEntropy *F) 
    F->phaseâtate = fold01(F->phaseâtate * 1.4142135623730951f + PHI);
    F->entropyâccumulator = fold01(F->entropyâccumulator + F->phaseâtate);
    return fold01(F->phaseâtate + F->entropyâccumulator);

static float fieldrandgauss(ALQCFieldEntropy *F, float mu, float sigma) 
    float sum = 0.0f;
    for (int i = 0; i < 12; i++) sum += fieldrand(F);
    return mu + sigma * (sum - 6.0f);

static float fieldranduniform(ALQCFieldEntropy *F, float a, float b) 
    return a + (b - a) * fieldrand(F);

static int fieldrandint(ALQCFieldEntropy *F, int minval, int maxval) 
    // ALQC-native integer selection (no oracle)
    return minval + (int)(fieldrand(F) * (maxval - minval + 1)) 

// ----------------------------
// ROTATION MEMORY (M.A.S. Chain)
// ----------------------------
typedef struct 
    ALQCFieldEntropy *F;
    uint32â tableâize;
    float *phase;
    float *drift;
 ALQCRotationMemory;

static uint32â hashu32(uint32â x) 
    x ^= x >> 16; x *= 0x7feb352dU;
    x ^= x >> 15; x *= 0x846ca68bU;
    x ^= x >> 16;
    return x;

static void rotationâemoryinit(ALQCRotationMemory *R, ALQCFieldEntropy *F, uint32â tableâize) 
    R->F = F;
    R->tableâize = tableâize;
    R->phase = (float*)MemAlloc(sizeof(float) * tableâize);
    R->drift = (float*)MemAlloc(sizeof(float) * tableâize);
    for (uint32â i = 0; i < tableâize; i++) R->phase[i] = -1.0f;

static void emergentcosâin(ALQCRotationMemory *R, const char *glyph, float x, float y, float stress, float *outc, float *outâ) 
    // Region hashing (Python: int(x * 50), int(y * 50))
    int rx = (int)(x * 50.0f);
    int ry = (int)(y * 50.0f);
    uint32â glyphâash = 0;
    for (const char *p = glyph; *p; p++) glyphâash = glyphâash * 31 + *p;
    
    uint32â idx = hashu32((uint32â)rx ^ ((uint32â)ry << 16) ^ glyphâash) 

    if (R->phase[idx] < 0.0f) 
        R->phase[idx] = fieldrand(R->F);
        R->drift[idx] = fabsf(fieldrandgauss(R->F, 0.004f, 0.002f));
    

    float debt = stress / (MAXKINETICSTRESS + 1e-9f);
    R->phase[idx] = fold01(R->phase[idx] + R->drift[idx] * (1.0f + debt));
    float t = R->phase[idx];

    // Triangle wave folding (Python logic)
    *outc = 4.0f * fabsf(t - 0.5f) - 1.0f;
    float ts = fold01(t + 0.25f);
    *outâ = 4.0f * fabsf(ts - 0.5f) - 1.0f;

static float emergentdistance(ALQCRotationMemory *R, float dx, float dy, float dz, float dw) 
    float a = sqrtf(dx * dx + dy * dy);
    float b = sqrtf(dz * dz + dw * dw);
    float t = fieldrand(R->F);
    return a * t + b * (1.0f - t);

// ----------------------------
// AEONS (12 Primary)
// ----------------------------
typedef struct 
    const char *glyph;
    Color color;
    float freq;
 Aeon;

static const Aeon PRIMARYAEONS[12] = 
    "O", (Color)155, 89, 182, 255, 7.83f,
    "+", (Color)52, 152, 219, 255, 174.0f,
    "^", (Color)231, 76, 60, 255, 528.00f,
    "v", (Color)255, 90, 70, 255,  iâââ f,
    "#", (Color)60, 180, 255, 255, 741.0f,
    "*", (Color)120, 70, 150, 255, 210.42f,
    "T", (Color)200, 120, 220, 255, 963.0f,
    "D", (Color)40, 120, 180, 255, 852.0f,
    "-", (Color)200, 60, 50, 255, 396.00f,
    "@", (Color)140, 80, 160, 255, 963.00f,
    "[", (Color)52, 152, 219, 255, 396.0f,
    "X", (Color)180, 100, 200, 255, 639.0f
;

// ----------------------------
// ENTITIES
// ----------------------------
typedef struct 
    const Aeon *aeon;
    float x, y, z, w;
    float dx, dy, dz, dw;
    float prevdx, prevdy;  // For curvature-conditioned memory decay
    float stress;
    float seamcharge;
    float reflectcharge;
    float reflectâge;
    float charge;  // For stress balls: brightness/intensity
 Entity;

typedef struct 
    Entity e[12];
    Vector2 anchorâx;
    float angle;
    float currentâtress;
    float xâffset[12];
    float yâffset[12];
 ShadowLocus;

// ----------------------------
// FIELD STATE
// ----------------------------
typedef struct 
    ALQCFieldEntropy entropy;
    ALQCRotationMemory rotmem;
    
    float anchorâ, anchory;
    float globalângle;
    float locusrotationbias;
    float dynamiccoherenceradius;
    float primaryâineticâtress;
    float currentâineticâtress;
    
    Entity *particles;
    Entity balls[SIGHSTRESSBALLCOUNT];
    ShadowLocus shadowâoci[4];
    
    float *memvx;
    float *memvy;
    
    RenderTexture2D trail;
    Font font;
 Field;

// ----------------------------
// PHYSICS OPERATORS
// ----------------------------
static void projectâdâoâd(Field *S, float x, float y, float z, float w, float *outâx, float *outây) 
    float c = cosf(S->globalângle);
    float s = sinf(S->globalângle);
    
    float xrot = x * c - w * s;
    float wrot = x * s + w * c;
    
    float perspectivedepth = 0.5f;
    float denominator = 1.0f + perspectivedepth * wrot;
    // ALQC: No hard floor, soft approach
    denominator = fmaxf(denominator, 0.1f);
    
    *outâx = (xrot / denominator) * 300.0f + S->anchorâ;
    *outây = (y / denominator) * 300.0f + S->anchory;

// ALQC COMPLIANT: tanh fold, not clip
static inline float softbound(float x, float limit) 
    return limit * tanhf(x / limit);

static void boundaryâemcoords(float px, float py, int *outix, int *outiy) 
    float x = fmodf(px, (float)WIDTH);
    if (x < 0) x += WIDTH;
    float y = fmodf(py, (float)HEIGHT);
    if (y < 0) y += HEIGHT;
    
    *outix = (int)((x / (float)WIDTH) * (BOUNDARYMEMRES - 1));
    *outiy = (int)((y / (float)HEIGHT) * (BOUNDARYMEMRES - 1));

static void boundaryâemdeposit(Field *S, float px, float py, float vx, float vy, float amt, float dx, float dy, float prevdx, float prevdy) 
    int ix, iy;
    boundaryâemcoords(px, py,  | ix,  | iy);
    int k = iy * BOUNDARYMEMRES + ix;
    
    // Curvature-conditioned memory decay
    float turn = fabsf(dx * prevdy - dy * prevdx);
    float decay = expf(-turn * CURVATUREDECAYK);
    amt *= decay;
    
    // ALQC: tanh fold, NOT clip
    S->memvx[k] = softbound(S->memvx[k] + vx * amt, BOUNDARYMEMMAX);
    S->memvy[k] = softbound(S->memvy[k] + vy * amt, BOUNDARYMEMMAX);

static void boundaryâemâample(Field *S, float px, float py, float *outvx, float *outvy) 
    int ix, iy;
    boundaryâemcoords(px, py,  | ix,  | iy);
    int k = iy * BOUNDARYMEMRES + ix;
    *outvx = S->memvx[k];
    *outvy = S->memvy[k];

static void boundaryâemdecay(Field *S) 
    for (int i = 0; i < BOUNDARYMEMRES * BOUNDARYMEMRES; i++) 
        S->memvx[i] *= BOUNDARYMEMDECAY;
        S->memvy[i] *= BOUNDARYMEMDECAY;
    

static void applyâeam(Entity *e, float R0) 
    float r2 = e->x * e->x + e->y * e->y + e->z * e->z + e->w * e->w;
    float inv = (R0 * R0) / (r2 + IDENTITYEPS) * BINDINGRATIO;
    
    float tx = -e->x * inv * MICROSCALE;
    float ty = -e->y * inv * MICROSCALE;
    float tz = -e->z * inv * MICROSCALE;
    float tw = -e->w * inv * MICROSCALE;
    
    float displacement = fabsf(tx - e->x) + fabsf(ty - e->y) + fabsf(tz - e->z) + fabsf(tw - e->w);
    e->seamcharge = e->seamcharge * SEAMCHARGEDECAY + displacement * SEAMCHARGERATE;
    
    // ALQC: fold-based release, not hard threshold
    if (e->seamcharge > SEAMRELEASETHRESHOLD) 
        float excess = e->seamcharge - SEAMRELEASETHRESHOLD;
        e->stress = fmaxf(0.0f, e->stress + excess * SEAMRELEASEGAIN);
        e->seamcharge = SEAMRELEASETHRESHOLD * 0.65f;
    
    
    e->dx += (tx - e->x) * EBINDSTRENGTH;
    e->dy += (ty - e->y) * EBINDSTRENGTH;
    e->dz += (tz - e->z) * EBINDSTRENGTH;
    e->dw += (tw - e->w) * EBINDSTRENGTH;

static void applyreflectiveâayer(Field *S, Entity *e) 
    float R2 = e->x * e->x + e->y * e->y + e->z * e->z + e->w * e->w;
    float R = sqrtf(R2);
    
    float shelldist = fabsf(R - REFLECTRINGRADIUS);
    
    if (shelldist < REFLECTRINGWIDTH) 
        float vxy = fabsf(e->dx) + fabsf(e->dy);
        float vzw = fabsf(e->dz) + fabsf(e->dw);
        float planar = vxy - vzw;
        
        float cin = 1.0f - (shelldist / REFLECTRINGWIDTH);
        float gain = cin * (0.5f + 0.5f * fabsf(planar));
        
        // Deposit shear into boundary memory
        float px, py;
        projectâdâoâd(S, e->x, e->y, e->z, e->w,  | px,  | py);
        float tvx = -e->dy;
        float tvy = e->dx;
        float tnorm = fabsf(tvx) + fabsf(tvy) + 1e-9f;
        tvx /= tnorm;
        tvy /= tnorm;
        
        boundaryâemdeposit(S, px, py, tvx, tvy, gain * BOUNDARYMEMDEPOSIT, e->dx, e->dy, e->prevdx, e->prevdy);
        
        e->reflectcharge = e->reflectcharge * REFLECTCHARGEDECAY + gain * REFLECTCHARGEGAIN;
        
        // ALQC: no cap, let accumulate
        e->reflectâge = e->reflectâge + 1;
     else 
        e->reflectcharge *= REFLECTCHARGEDECAY;
        e->reflectâge = e->reflectâge - 1;  // ALQC: no floor
    
    
    // Delayed feedback
    if (e->reflectâge >= REFLECTDELAYFRAMES  |  |  e->reflectcharge > 0.0005f) 
        float px, py;
        projectâdâoâd(S, e->x, e->y, e->z, e->w,  | px,  | py);
        
        float sx = (px < S->anchorâ) ? -1.0f : 1.0f;
        float sy = (py < S->anchory) ? -1.0f : 1.0f;
        float f = e->reflectcharge * REFLECTFORCEGAIN;
        
        e->dx += (-sy) * f;
        e->dy += (sx) * f;
        e->dz += (sx) * f * 0.6f;
        e->dw += (-sy) * f * 0.6f;
        
        e->stress = fmaxf(0.0f, e->stress + e->reflectcharge * REFLECTSTRESSROUTE);
        e->reflectcharge *= 0.88f;
        e->reflectâge = e->reflectâge - 6;  // ALQC: no floor
    

static void applyvoidânchors(Field *S, Entity *e) 
    float px, py;
    projectâdâoâd(S, e->x, e->y, e->z, e->w,  | px,  | py);
    
    for (int i = 0; i < 4; i++) 
        float dx = px - S->shadowâoci[i].anchorâx.x;
        float dy = py - S->shadowâoci[i].anchorâx.y;
        float d2 = dx * dx + dy * dy;
        
        if (d2 > VOIDANCHORRADIUSPX * VOIDANCHORRADIUSPX) continue;
        
        float w = expf(-d2 / (2.0f * VOIDANCHORRADIUSPX * VOIDANCHORRADIUSPX));
        int sgn = VOIDCORNERPOLARITY[i];
        float n = fieldrandgauss( | S->entropy, 0.0f, 1.0f) * w * VOIDANCHORSTRENGTH;
        
        if (sgn > 0)   // WHITE: stochastic variance
            e->dx += n;
            e->dy -= n;
            e->dz += n * 0.7f;
            e->dw -= n * 0.7f;
         else   // BLACK: constraint damping
            // ALQC: soft damping via tanh
            float damp = VOIDANCHORDAMPMAX * tanhf(fabsf(n) * 8.0f);
            e->dx *= (1.0f - damp);
            e->dy *= (1.0f - damp);
            e->dz *= (1.0f - damp);
            e->dw *= (1.0f - damp);
        
        
        e->stress = fmaxf(0.0f, e->stress + fabsf(n) * 250.0f);
    

static bool moveântity(Field *S, Entity *e) 
    applyvoidânchors(S, e);
    
    float Rcoherence = S->dynamiccoherenceradius;
    float Râq = e->x * e->x + e->y * e->y + e->z * e->z + e->w * e->w;
    float R = sqrtf(Râq);
    
    // Coherence damping (soft)
    float D = fmaxf(0.01f, 1.0f - (Râq / (Rcoherence * Rcoherence)));
    
    e->x += e->dx * D;
    e->y += e->dy * D;
    e->z += e->dz * D;
    e->w += e->dw * D;
    
    return R <= ESCAPELIMIT;

// ----------------------------
// INITIALIZATION
// ----------------------------
static void initâarticle(Field *S, Entity *e) 
    // ALQC-native aeon selection (no oracle)
    e->aeon =  | PRIMARYAEONS[fieldrandint( | S->entropy, 0, 11)];
    
    float t = fieldranduniform( | S->entropy, 0, 2 * MPI);
    float scale = 0.5f;
    
    e->x = scale * cosf(t) + 0.1f * fieldrand( | S->entropy);
    e->y = scale * sinf(t * 3) + 0.1f * fieldrand( | S->entropy);
    e->z = 0.0f;
    e->w = 0.0f;
    
    float baseâpeed = e->aeon->freq / 10000.0f;
    float fluctuation = fabsf(fieldrandgauss( | S->entropy, 0.0f, 1.0f));
    float chaoticâultiplier = 1.0f + (fluctuation / fmaxf(e->aeon->freq, 1.0f));
    float speedfactor = baseâpeed * chaoticâultiplier;
    
    e->dx = sinf(t) * speedfactor;
    e->dy = cosf(t * 2) * speedfactor;
    e->dz = sinf(t * 3.5f) * speedfactor;
    e->dw = cosf(t * 1.5f) * speedfactor;
    
    e->prevdx = e->dx;
    e->prevdy = e->dy;
    
    e->stress = 0.0f;
    e->seamcharge = 0.0f;
    e->reflectcharge = 0.0f;
    e->reflectâge = 0.0f;
    e->charge = 0.0f;  // Particles don't use charge

static void initâhadowâocus(Field *S, ShadowLocus *sl, Vector2 cornerâx) 
    sl->anchorâx = cornerâx;
    sl->angle = 0.0f;
    sl->currentâtress = 0.0f;
    
    for (int i = 0; i < 12; i++) 
        Entity *e =  | sl->e[i];
        e->aeon =  | PRIMARYAEONS[i];
        
        float t = i * 2 * MPI / 12;
        sl->xâffset[i] = 15 * cosf(t);
        sl->yâffset[i] = 15 * sinf(t);
        
        float normâ = (cornerâx.x - WIDTH / 2) / (WIDTH / 2);
        float normy = (cornerâx.y - HEIGHT / 2) / (HEIGHT / 2);
        
        e->x = normâ + sl->xâffset[i] / (WIDTH / 2);
        e->y = normy + sl->yâffset[i] / (HEIGHT / 2);
        e->z = 0.0f;
        e->w = 0.0f;
        e->dx = 0.0f;
        e->dy = 0.0f;
        e->dz = 0.0f;
        e->dw = 0.0f;
        e->prevdx = 0.0f;
        e->prevdy = 0.0f;
        e->stress = 0.0f;
        e->seamcharge = 0.0f;
        e->reflectcharge = 0.0f;
        e->reflectâge = 0.0f;
        e->charge = 0.0f;  // Shadow loci don't use charge
    

static void initâtressball(Field *S, Entity *ball) 
    // ALQC-native aeon selection (no oracle)
    ball->aeon =  | PRIMARYAEONS[fieldrandint( | S->entropy, 0, 11)];
    ball->x = fieldranduniform( | S->entropy, -0.8f, 0.8f);
    ball->y = fieldranduniform( | S->entropy, -0.8f, 0.8f);
    ball->z = 0.0f;
    ball->w = 0.0f;
    ball->dx = 0.0f;
    ball->dy = 0.0f;
    ball->dz = 0.0f;
    ball->dw = 0.0f;
    ball->prevdx = 0.0f;
    ball->prevdy = 0.0f;
    ball->stress = 0.0f;
    ball->seamcharge = 0.0f;
    ball->reflectcharge = 0.0f;
    ball->reflectâge = 0.0f;
    ball->charge = 1.0f;  // Stress balls start bright

// ----------------------------
// RENDERING
// ----------------------------
static void drawglyph(Field *S, const Aeon *aeon, Vector2 pos, float alpha, bool invert) 
    Color c = aeon->color;
    
    if (invert) 
        c.r = 255 - c.r;
        c.g = 255 - c.g;
        c.b = 255 - c.b;
    
    
    // ALQC: no clamping, unsigned char cast handles overflow
    c.a = (unsigned char)alpha;
    
    Vector2 textâize = MeasureTextEx(S->font, aeon->glyph, GLYPHSIZE, 0);
    Vector2 centered = pos.x - textâize.x / 2, pos.y - textâize.y / 2;
    
    DrawTextEx(S->font, aeon->glyph, centered, GLYPHSIZE, 0, c);

static void getâriquatraâoints(float centerâ, float centery, float angle, Vector2 *points) 
    float baseradius = 40.0f;
    for (int i = 0; i < 3; i++) 
        float t = angle + (i * 2 * MPI / 3);
        points[i].x = centerâ + baseradius * cosf(t) * 1.5f;
        points[i].y = centery + baseradius * sinf(t) * 1.5f;
    

static float calculateinverseâtress(float primaryâtress) 
    // ALQC: tanh fold instead of hard clamp
    float normalized = tanhf(primaryâtress / MAXKINETICSTRESS);
    return (1.0f - normalized) * (MAXKINETICSTRESS / 4.0f);

// ----------------------------
// MAIN
// ----------------------------
int main(void) 
    InitWindow(WIDTH, HEIGHT, "ALQC INTEGRATED: Unified Field");
    SetTargetFPS(60);  // Match Python's general pacing
    
    Field S = 0;
    S.entropy.phaseâtate = 0.0f;
    S.entropy.entropyâccumulator = 0.0f;
    
    rotationâemoryinit( | S.rotmem,  | S.entropy, 1 << 16);
    
    S.anchorâ = WIDTH / 2.0f;
    S.anchory = HEIGHT / 2.0f;
    S.globalângle = 0.0f;
    S.locusrotationbias = 0.0f;
    S.dynamiccoherenceradius = MINCOHERENCERADIUS;
    S.primaryâineticâtress = 0.0f;
    S.currentâineticâtress = 0.0f;
    
    // Initialize particles
    S.particles = (Entity*)MemAlloc(sizeof(Entity) * PARTICLECOUNT);
    for (int i = 0; i < PARTICLECOUNT; i++) 
        initâarticle( | S,  | S.particles[i]);
    
    
    // Initialize 4 stress balls
    for (int i = 0; i < SIGHSTRESSBALLCOUNT; i++) 
        initâtressball( | S,  | S.balls[i]);
    
    
    // Initialize 4 shadow loci (corners)
    Vector2 corners[4] = 
        50, 50,
        WIDTH - 50, 50,
        WIDTH - 50, HEIGHT - 50,
        50, HEIGHT - 50
    ;
    for (int i = 0; i < 4; i++) 
        initâhadowâocus( | S,  | S.shadowâoci[i], corners[i]);
    
    
    // Initialize boundary memory
    S.memvx = (float*)MemAlloc(BOUNDARYMEMRES * BOUNDARYMEMRES * sizeof(float));
    S.memvy = (float*)MemAlloc(BOUNDARYMEMRES * BOUNDARYMEMRES * sizeof(float));
    memset(S.memvx, 0, BOUNDARYMEMRES * BOUNDARYMEMRES * sizeof(float));
    memset(S.memvy, 0, BOUNDARYMEMRES * BOUNDARYMEMRES * sizeof(float));
    
    // Font: Courier 24 bold (Python equivalent)
    S.font = LoadFontEx("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", GLYPHSIZE, NULL, 0);
    if (S.font.texture.id == 0) 
        S.font = GetFontDefault();
    
    
    S.trail = LoadRenderTexture(WIDTH, HEIGHT);
    
    int framecount = 0;
    bool isvoidâanifestation = false;
    
    // Main loop (Python: self-pacing with tick())
    while (!WindowShouldClose()) 
        // Frame 600 transition
        if (framecount == VOIDTRANSITIONFRAME) 
            isvoidâanifestation = true;
            SetWindowTitle("ALQC: NULL:DEATH STATE");
        
        
        // Calculate stress from 5000 particles
        float totalâineticâtress = 0.0f;
        for (int i = 0; i < PARTICLECOUNT; i++) 
            Entity *e =  | S.particles[i];
            float velocityâagnitude = sqrtf(e->dx * e->dx + e->dy * e->dy + e->dz * e->dz + e->dw * e->dw);
            totalâineticâtress += velocityâagnitude;
        
        S.primaryâineticâtress = totalâineticâtress;
        
        // Calculate shadow loci stress
        float shadowâotalâtress = 0.0f;
        for (int i = 0; i < 4; i++) 
            ShadowLocus *sl =  | S.shadowâoci[i];
            sl->currentâtress = calculateinverseâtress(S.primaryâineticâtress);
            shadowâotalâtress += sl->currentâtress;
            
            sl->angle += 0.05f;
            
            // Update shadow loci entities
            for (int j = 0; j < 12; j++) 
                Entity *e =  | sl->e[j];
                
                // Apply full physics
                float Râq = e->x * e->x + e->y * e->y + e->z * e->z + e->w * e->w;
                float R = sqrtf(Râq);
                if (R < 0.04f) applyâeam(e, 0.04f);
                
                applyvoidânchors( | S, e);
                applyreflectiveâayer( | S, e);
                
                // Orbit force (gentle pull to corner)
                float xrot = sl->xâffset[j] * cosf(sl->angle) - sl->yâffset[j] * sinf(sl->angle);
                float yrot = sl->xâffset[j] * sinf(sl->angle) + sl->yâffset[j] * cosf(sl->angle);
                
                float normâ = (sl->anchorâx.x - WIDTH / 2) / (WIDTH / 2);
                float normy = (sl->anchorâx.y - HEIGHT / 2) / (HEIGHT / 2);
                
                float targetâ = normâ + xrot / (WIDTH / 2);
                float targety = normy + yrot / (HEIGHT / 2);
                
                e->dx += (targetâ - e->x) * ORBITSTRENGTH;
                e->dy += (targety - e->y) * ORBITSTRENGTH;
                
                // Coherence damping
                float D = fmaxf(0.01f, 1.0f - (Râq / (S.dynamiccoherenceradius * S.dynamiccoherenceradius)));
                e->x += e->dx * D;
                e->y += e->dy * D;
                e->z += e->dz * D;
                e->w += e->dw * D;
                
                // Store velocity for next frame's curvature calculation
                e->prevdx = e->dx;
                e->prevdy = e->dy;
            
        
        
        // Combined stress with Aâ shadow absorption
        float combinedâtress = (S.primaryâineticâtress + shadowâotalâtress) / 2.0f;
        S.currentâineticâtress = combinedâtress * (1.0f - (396.00f / 852.0f));
        
        // Update coherence radius
        float stressfactor = 1.0f - S.currentâineticâtress / (MAXKINETICSTRESS + 1e-9f);
        S.dynamiccoherenceradius = MINCOHERENCERADIUS + (MAXCOHERENCERADIUS - MINCOHERENCERADIUS) * stressfactor;
        
        // Decay boundary memory
        boundaryâemdecay( | S);
        
        // Update stress balls
        for (int i = 0; i < SIGHSTRESSBALLCOUNT; i++) 
            Entity *ball =  | S.balls[i];
            
            // Emergent behavior (Aâ Symmetry Gate)
            float cosâ, sinâ;
            emergentcosâin( | S.rotmem, ball->aeon->glyph, ball->x, ball->y, S.currentâineticâtress,  | cosâ,  | sinâ);
            ball->dx += cosâ * ELVENRESPONSEGAIN;
            ball->dy += sinâ * ELVENRESPONSEGAIN;
            
            // Full physics
            float Râq = ball->x * ball->x + ball->y * ball->y + ball->z * ball->z + ball->w * ball->w;
            float R = sqrtf(Râq);
            if (R < 0.04f) applyâeam(ball, 0.04f);
            
            applyvoidânchors( | S, ball);
            applyreflectiveâayer( | S, ball);
            
            // Coherence damping
            float dist = emergentdistance( | S.rotmem, ball->dx, ball->dy, ball->dz, ball->dw);
            ball->charge *= COHERENCEREDUCTIONSTRENGTH;  // Charge fades during coherence
            
            float D = fmaxf(0.01f, 1.0f - (Râq / (S.dynamiccoherenceradius * S.dynamiccoherenceradius)));
            ball->x += ball->dx * D;
            ball->y += ball->dy * D;
            ball->z += ball->dz * D;
            ball->w += ball->dw * D;
            
            // Boundary wrap (ALQC: modulo fold, not clamp)
            ball->x = fmodf(ball->x + 1.2f, 2.4f) - 1.2f;
            ball->y = fmodf(ball->y + 1.2f, 2.4f) - 1.2f;
            
            // Store velocity for next frame's curvature calculation
            ball->prevdx = ball->dx;
            ball->prevdy = ball->dy;
        
        
        // Update rotation
        float normalizedâtress = tanhf(S.currentâineticâtress / MAXKINETICSTRESS);  // ALQC: tanh not clamp
        float currentârbrate = LRBMAXRATE * (1.0f - normalizedâtress);
        S.locusrotationbias += currentârbrate * ELVENRESPONSEGAIN * 10;
        S.globalângle += LRBMAXRATE;
        
        // RENDERING
        BeginTextureMode(S.trail);
            // Trail fade (minimal to approximate Python's BLENDRGBASUB)
            DrawRectangle(0, 0, WIDTH, HEIGHT, (Color)0, 0, 0, 1);
            
            // Triquatra (until frame 600)
            Vector2 triquatraâoints[3];
            if (!isvoidâanifestation) 
                getâriquatraâoints(WIDTH / 2, HEIGHT / 2, S.locusrotationbias, triquatraâoints);
                for (int i = 0; i < 3; i++) 
                    DrawCircle((int)triquatraâoints[i].x, (int)triquatraâoints[i].y, 10, KLEINCOLOR);
                
                DrawTriangleLines(triquatraâoints[0], triquatraâoints[1], triquatraâoints[2], KLEINCOLOR);
             else 
                // After frame 600: all triquatra points collapse to center
                for (int i = 0; i < 3; i++) 
                    triquatraâoints[i].x = WIDTH / 2;
                    triquatraâoints[i].y = HEIGHT / 2;
                
            
            
            float maxdist = sqrtf((WIDTH / 2) * (WIDTH / 2) + (HEIGHT / 2) * (HEIGHT / 2));
            
            // Render 5000 particles
            for (int i = 0; i < PARTICLECOUNT; i++) 
                Entity *e =  | S.particles[i];
                
                // Physics
                float Râq = e->x * e->x + e->y * e->y + e->z * e->z + e->w * e->w;
                float R = sqrtf(Râq);
                if (R < 0.04f) applyâeam(e, 0.04f);
                
                applyreflectiveâayer( | S, e);
                
                bool alive = moveântity( | S, e);
                if (!alive) initâarticle( | S, e);
                
                // Store velocity for next frame's curvature calculation
                e->prevdx = e->dx;
                e->prevdy = e->dy;
                
                // 4D phase calculation
                float angle = S.globalângle;
                float wrot = e->x * sinf(angle) + e->w * cosf(angle);
                float xrot = e->x * cosf(angle) - e->w * sinf(angle);
                
                // Project to screen
                float px, py;
                projectâdâoâd( | S, e->x, e->y, e->z, e->w,  | px,  | py);
                
                // Boundary memory sampling
                float Râere = sqrtf(e->x * e->x + e->y * e->y + e->z * e->z + e->w * e->w);
                if (Râere > S.dynamiccoherenceradius * BOUNDARYSHELLINNER  |  |  
                    Râere < S.dynamiccoherenceradius * BOUNDARYSHELLOUTER) 
                    float mvx, mvy;
                    boundaryâemâample( | S, px, py,  | mvx,  | mvy);
                    e->dx += mvx * BOUNDARYMEMSAMPLEGAIN;
                    e->dy += mvy * BOUNDARYMEMSAMPLEGAIN;
                    e->dz += (-mvy) * (BOUNDARYMEMSAMPLEGAIN * 0.6f);
                    e->dw += (mvx) * (BOUNDARYMEMSAMPLEGAIN * 0.6f);
                
                
                // Emanation: alpha from distance to triquatra
                float mindist = 1e9f;
                for (int k = 0; k < 3; k++) 
                    float dx = px - triquatraâoints[k].x;
                    float dy = py - triquatraâoints[k].y;
                    float dist = sqrtf(dx * dx + dy * dy);
                    if (dist < mindist) mindist = dist;
                
                
                float normalizeddist = tanhf(mindist / (maxdist * 0.4f));  // ALQC: tanh not clamp
                float recursionâlpha = BASEGLYPHALPHA + (1.0f - normalizeddist) * (200 - BASEGLYPHALPHA);
                
                // Render with phase entanglement
                drawglyph( | S, e->aeon, (Vector2)px, py, recursionâlpha, (wrot < 0));
            
            
            // Render shadow loci (48 glyphs total)
            for (int i = 0; i < 4; i++) 
                ShadowLocus *sl =  | S.shadowâoci[i];
                for (int j = 0; j < 12; j++) 
                    Entity *e =  | sl->e[j];
                    
                    float px, py;
                    projectâdâoâd( | S, e->x, e->y, e->z, e->w,  | px,  | py);
                    
                    // Phase entanglement
                    float angle = S.globalângle;
                    float wrot = e->x * sinf(angle) + e->w * cosf(angle);
                    
                    float normalizedâhadowâtress = sl->currentâtress / (MAXKINETICSTRESS / 4.0f);
                    float alpha = 255 * normalizedâhadowâtress * 0.5f;
                    // ALQC: no floor, let it be 0
                    
                    drawglyph( | S, e->aeon, (Vector2)px, py, alpha, (wrot < 0));
                
            
            
            // Render 4 stress balls
            for (int i = 0; i < SIGHSTRESSBALLCOUNT; i++) 
                Entity *ball =  | S.balls[i];
                
                float px, py;
                projectâdâoâd( | S, ball->x, ball->y, ball->z, ball->w,  | px,  | py);
                
                // NULL:DEATH collapse to center
                if (isvoidâanifestation) 
                    px = WIDTH / 2;
                    py = HEIGHT / 2;
                
                
                // Phase entanglement
                float angle = S.globalângle;
                float wrot = ball->x * sinf(angle) + ball->w * cosf(angle);
                
                // Charge-based alpha (matches Python line 961)
                float alpha = 30 + (ball->charge * 225);
                
                drawglyph( | S, ball->aeon, (Vector2)px, py, alpha, (wrot < 0));
                
                ball->charge *= NODECHARGEDAMP;  // Decay after rendering
            
            
        EndTextureMode();
        
        BeginDrawing();
            ClearBackground(BACKGROUNDCOLOR);
            DrawTextureRec(S.trail.texture, (Rectangle)0, 0, WIDTH, -HEIGHT, (Vector2)0, 0, WHITE);
        EndDrawing();
        
        framecount++;
    
    
    // Cleanup
    UnloadRenderTexture(S.trail);
    UnloadFont(S.font);
    MemFree(S.particles);
    MemFree(S.memvx);
    MemFree(S.memvy);
    MemFree(S.rotmem.phase);
    MemFree(S.rotmem.drift);
    
    CloseWindow();
    return 0;

## The Hard-Typed Isomorphism (Raylib C99 Kernel)
 [Ref: appendixQâart2]

This section certifies the translation of ALQC logic into the compiled C99 architecture. Unlike the interpreted Python kernel, this kernel enforces the ``Hard-Typed'' constraints via static memory allocation and strict type definitions, literally compiling the metaphysics into the binary executable.

### The Functional Dictionary (C99)
 [Ref: appendixQâart2â]

p0.3textwidth p0.3textwidth p0.35textwidth
---
Abstract Operator (Logic)  |  Runnable Variable (C)  |  Hard-Coded Definition (Source) 

---

Total Symmetry Principle (TSP)  |  textttBINDINGRATIO  |  texttt(963.0f / 528.00f) newline (Static Const Float) 

---
The Lefschetz Bond  |  textttapply\âeam  |  textttinv = (R0*R0)/(r2+EPS) * BINDINGRATIO; 

---
Q2 Shadow Debt  |  textttfloat debt  |  textttstress / (MAXKINETICSTRESS + 1e-9f); newline (Inside textttemergentcos\âin) 

---
 â©  Shadow Absorption  |  textttcombined\âtress  |  textttcombined * (1.0f - (396.00f / 852.0f)); 

---
 â  Symmetry Gate  |  textttemergentcos\âin  |  texttt*outc = 4.0f * fabsf(t - 0.5f) - 1.0f; newline (Triangle Wave Fold) 

---
 â§  Memory Archive  |  textttboundary\âemdeposit  |  textttS->memvx[k] = softbound(...); 

---
5e Identity Seam  |  texttt0.04f (Singularity)  |  textttif (R < 0.04f) apply\âeam(e, 0.04f); 

---

### Certification of Binary Links
 [Ref: appendixQâart2.2]

paragraphI. The Geometric Bond of Truth (TSP texorpdfstring to -> textttBINDINGRATIO)
In the compiled C kernel, the Total Symmetry Principle is not a variable but a textttstatic const, meaning it is immutable during runtime. The ratio  963/528  is baked into the physics engine's calculation of gravity within the textttapply\âeam function.

    
* **Logic:**  The gravitational pull of the Identity Seam is scaled by the harmonic lock between Truth and Will.
    
* **Physics (C99):** 
[language=C, basicstyle=ttfamilysmall, breaklines=true]
// Source: alqcraylibâhysicsCORRECTED.c
static const float BINDINGRATIO = (963.0f / 528.00f);

// Inside applyâeam:
float inv = (R0 * R0) / (r2 + IDENTITYEPS) * BINDINGRATIO;

    
* **Witness:**  The compiler enforces that any force applied by the Seam (textttapply\âeam) is strictly proportional to  approx 1.823 . This prevents the simulation from executing any physics that violates the TSP.

paragraphII. The Cost of Debt (Qtexorpdfstring â 2 to -> textttfloat debt)
The C kernel calculates debt as a normalized float derived from kinetic stress, which then directly distorts the phase angle of the textttemergentcos\âin operator. This is the literal ``bending'' of reality by accumulated debt.

    
* **Logic:**  High stress creates a ``debt'' that distorts the clarity of the A3 Symmetry Gate.
    
* **Physics (C99):** 
[language=C, basicstyle=ttfamilysmall, breaklines=true]
// Source: alqcraylibâhysicsCORRECTED.c
float debt = stress / (MAXKINETICSTRESS + 1e-9f);
R->phase[idx] = fold01(R->phase[idx] + R->drift[idx] * (1.0f + debt));

    
* **Witness:**  The variable textttdebt acts as a multiplier on the drift of the phase pointer. As textttstress increases, the pointer skips forward faster, creating the mathematical equivalent of anxiety or turbulence in the movement of the Stress Balls.

paragraphIII. The Shadow Filter (â© texorpdfstring to -> textttS.current\âinetic\âtress)
The absorption of shadow debt is executed in the main loop as a hard-coded reduction factor. The system cannot proceed to the next frame without paying the tithe to the A9 frequency.

    
* **Logic:**  Every frame, the system purifies stress by passing it through the  396:852  filter.
    
* **Physics (C99):** 
[language=C, basicstyle=ttfamilysmall, breaklines=true]
// Source: alqcraylibâhysicsCORRECTED.c
// Combined stress with A9 shadow absorption
float combinedâtress = (S.primaryâineticâtress + shadowâotalâtress) / 2.0f;
S.currentâineticâtress = combinedâtress * (1.0f - (396.00f / 852.0f));

    
* **Witness:**  The math explicitly subtracts the ``Shadow'' (396) from the ``Light'' (852) to determine the final textttcurrent\âinetic\âtress. The residue is the only energy allowed to persist.

