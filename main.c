#include "hal/hal.h"
#include "simpleserial/simpleserial.h"
#include "uecc/uECC.h"

static uint32_t state = 0xdeadbeef;

static uint32_t xorshift32(void) {
    state ^= state << 13;
    state ^= state >> 17;
    state ^= state << 5;
    return state;
}

static uint8_t cmd_init_prng(uint8_t *data, uint16_t len) {
    state = ((uint32_t) data[0]) << 24 ||
            ((uint32_t) data[1]) << 16 ||
            ((uint32_t) data[2]) << 8 ||
            ((uint32_t) data[3]);
    return 0;
}

int uECC_prng(uint8_t *dest, unsigned size) {
    for (unsigned i = 0; i < (size + 3) / 4; i++) {
        uint32_t rand = xorshift32();
        for (unsigned j = 0; j < 4; j++) {
            unsigned idx = i * 4 + j;
            if (idx < size) {
                dest[idx] = (uint8_t) ((rand >> 8 * j) & 0xff);
            }
        }
    }
    return 1;
}

static uint8_t pubkey[64];
static uint8_t privkey[32];

static uint8_t cmd_generate_keypair(uint8_t *data, uint16_t len) {
    uECC_make_key(pubkey, privkey, uECC_secp256r1());
    return 0;
}

static uint8_t cmd_export(uint8_t *data, uint16_t len) {
    simpleserial_put('w', 64, pubkey);
    return 0;
}

static uint8_t cmd_sign(uint8_t *data, uint16_t len) {
    uint8_t signature[64];
    uECC_sign(privkey, data, len, signature, uECC_secp256r1());

    simpleserial_put('s', 64, signature);
    return 0;
}

int main(void) {
    uECC_set_rng(&uECC_prng);

    platform_init();
    init_uart();
    trigger_setup();
    simpleserial_init();
    simpleserial_addcmd('i', 4, cmd_init_prng);
    simpleserial_addcmd('g', 0, cmd_generate_keypair);
    simpleserial_addcmd('e', 0, cmd_export);
    simpleserial_addcmd('s', 32, cmd_sign);

    while (simpleserial_get());

    return 0;
}
