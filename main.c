#include "hal/hal.h"
#include "simpleserial/simpleserial.h"
#include "uecc/uECC.h"

static void wait_a_bit(){
    for (int i = 0; i < F_CPU / 100; i++) {
        NOP()
    }
}

static uint32_t state = 0xdeadbeef;

static uint32_t xorshift32(void) {
    state ^= state << 13;
    state ^= state >> 17;
    state ^= state << 5;
    return state;
}

static uint8_t cmd_init_prng(uint8_t *data, uint16_t len) {
    state = ((uint32_t) data[0]) << 24 |
            ((uint32_t) data[1]) << 16 |
            ((uint32_t) data[2]) << 8 |
            ((uint32_t) data[3]);
    wait_a_bit();
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

#define CURVE_SIZE 24

static uECC_Curve curve;

static uint8_t pubkey[CURVE_SIZE * 2];
static uint8_t privkey[CURVE_SIZE];

static uint8_t cmd_generate_keypair(uint8_t *data, uint16_t len) {
    led_error(1);
    uECC_make_key(pubkey, privkey, curve);
    led_error(0);
    return 0;
}

static uint8_t cmd_export(uint8_t *data, uint16_t len) {
    led_error(1);
    wait_a_bit();
    simpleserial_put('x', CURVE_SIZE, pubkey);
    wait_a_bit();
    simpleserial_put('y', CURVE_SIZE, pubkey + CURVE_SIZE);
    //simpleserial_put('k', CURVE_SIZE, privkey);
    led_error(0);
    return 0;
}

static uint8_t cmd_sign(uint8_t *data, uint16_t len) {
    led_error(1);
    uint8_t signature[CURVE_SIZE * 2];
    trigger_high();
    uECC_sign(privkey, data, len, signature, curve);
    trigger_low();

    simpleserial_put('r', CURVE_SIZE, signature);
    wait_a_bit();
    simpleserial_put('s', CURVE_SIZE, signature + CURVE_SIZE);
    led_error(0);
    return 0;
}

int main(void) {
    uECC_set_rng(&uECC_prng);
    curve = uECC_secp192r1();

    platform_init();
    init_uart();
    trigger_setup();
    simpleserial_init();
    simpleserial_addcmd('i', 4, cmd_init_prng);
    simpleserial_addcmd('g', 0, cmd_generate_keypair);
    simpleserial_addcmd('e', 0, cmd_export);
    simpleserial_addcmd('s', 32, cmd_sign);

    led_ok(1);

    while (simpleserial_get());

    led_ok(0);

    return 0;
}
